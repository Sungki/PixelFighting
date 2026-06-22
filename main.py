import pygame
import sys
import math
from input import InputHandler
from physics import PhysicsEngine
from actor import ProceduralActor
from enemy import ProceduralEnemy  
from particle import ParticleSystem

class SoftBodyGameLauncher:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Procedural Fighter - Player KO Animation Integrated")
        self.clock = pygame.time.Clock()
        
        self.pixel_size = 6
        self.walk_speed = 6.5
        self.base_y = (self.height // self.pixel_size) // 2 + 5
        
        self.char_x = (self.width // self.pixel_size) // 4  
        self.direction = 1
        self.walk_weight = 0.0
        self.motion_time = 0.0
        self.was_grounded_last_frame = True
        
        self.player_hp = 100
        self.enemy_hp = 100
        
        self.player_ko_timer = 0.0
        
        self.inputs = InputHandler()
        self.physics = PhysicsEngine(self.base_y)
        self.actor = ProceduralActor()
        self.enemy = ProceduralEnemy(self.base_y)
        self.effects = ParticleSystem()
        
        self.color_bg = (17, 17, 22)
        self.color_ground = (44, 44, 53)
        self.ground_y_grid = int(self.base_y + 11)

    def draw_health_bars(self):
        pygame.draw.rect(self.screen, (30, 30, 35), (20, 20, 220, 20))
        pygame.draw.rect(self.screen, (30, 30, 35), (360, 20, 220, 20))
        pygame.draw.rect(self.screen, (150, 40, 40), (22, 22, 216, 16))
        pygame.draw.rect(self.screen, (150, 40, 40), (362, 22, 216, 16))
        
        p_bar_w = int(216 * (max(0, self.player_hp) / 100))
        e_bar_w = int(216 * (max(0, self.enemy_hp) / 100))
        
        if self.player_hp > 0:
            pygame.draw.rect(self.screen, (241, 196, 15), (22, 22, p_bar_w, 16))
        if self.enemy_hp > 0:
            pygame.draw.rect(self.screen, (241, 196, 15), (362 + (216 - e_bar_w), 22, e_bar_w, 16))

    def check_combat_collisions(self):
        if self.enemy_hp <= 0 or self.player_hp <= 0:
            return

        grid_distance = abs(self.char_x - self.enemy.char_x)
        
        if self.physics.is_kicking and 0.12 < self.physics.kick_time < 0.25 and not self.physics.has_hit_current_attack:
            if grid_distance <= 14.0:
                self.physics.has_hit_current_attack = True
                self.enemy.is_kicking = False  
                self.enemy.kick_time = 0.0
                self.enemy.char_x += self.direction * 16.0
                self.enemy.enemy_hp -= 20  
                self.enemy_hp = self.enemy.enemy_hp # Sync the top health bar display data
                
                spark_x = (self.char_x + self.enemy.char_x) / 2
                self.effects.spawn_kick_spark(spark_x, self.base_y, self.direction)
                self.effects.spawn_kick_spark(spark_x, self.base_y, -self.direction)

        if self.enemy.is_kicking and 0.12 < self.enemy.kick_time < 0.25:
            if grid_distance <= 14.0 and self.physics.hit_stun_timer <= 0:
                self.physics.take_damage(self.enemy.direction)
                self.player_hp -= 20
                
                spark_x = (self.char_x + self.enemy.char_x) / 2
                self.effects.spawn_kick_spark(spark_x, self.base_y, self.enemy.direction)
                self.effects.spawn_kick_spark(spark_x, self.base_y, -self.enemy.direction)

    def handle_player_movement(self, dt):
        if self.player_hp <= 0:
            self.physics.is_dead = True
            self.player_ko_timer += dt
            
            if self.player_ko_timer < 0.4:
                self.char_x += -self.enemy.direction * 22.0 * dt
                self.physics.ko_angle = (self.player_ko_timer / 0.4) * 1.57
                self.physics.jump_y = math.sin((self.player_ko_timer / 0.4) * math.pi) * 8.0
            else:
                self.physics.jump_y = 0.0
                self.physics.ko_angle = 1.57
                self.physics.flex_intensity = 1.2
            
            self.char_x %= (self.width // self.pixel_size)
            return

        if self.physics.hit_stun_timer <= 0:
            if self.inputs.check_jump():  self.physics.start_jump()
            if self.inputs.check_kick():  self.physics.start_kick()
                
            if self.inputs.is_key_held("Left"):    self.direction = -1
            elif self.inputs.is_key_held("Right"): self.direction = 1
            is_moving = self.inputs.is_key_held("Left") or self.inputs.is_key_held("Right")
        else:
            is_moving = False
        
        total_displacement = self.physics.update(dt)
        if self.physics.hit_stun_timer <= 0 and self.physics.is_kicking:
            self.char_x += self.direction * total_displacement
        else:
            self.char_x += total_displacement

        if self.physics.is_grounded and not self.was_grounded_last_frame:
            self.effects.spawn_dust(self.char_x, self.base_y + 10.5)
        self.was_grounded_last_frame = self.physics.is_grounded
        
        blend_speed = 8.0 * dt
        if is_moving:
            self.walk_weight = min(1.0, self.walk_weight + blend_speed)
            self.char_x += self.direction * 16.0 * dt
            time_mod = 0.3 if not self.physics.is_grounded else 1.0
            self.motion_time += dt * self.walk_speed * time_mod
        else:
            self.walk_weight = max(0.0, self.walk_weight - blend_speed)
            self.motion_time += dt * self.walk_speed * self.walk_weight

        max_grid_width = self.width // self.pixel_size
        self.char_x %= max_grid_width

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.inputs.process_event(event)

            self.screen.fill(self.color_bg)
            
            ground_y_pos = self.ground_y_grid * self.pixel_size
            pygame.draw.line(self.screen, self.color_ground, (0, ground_y_pos), (self.width, ground_y_pos), 2)
            
            dt = self.clock.tick(60) / 1000.0  
            current_time = pygame.time.get_ticks() / 1000.0
            
            self.handle_player_movement(dt)
            enemy_kick, enemy_k_time, enemy_x = self.enemy.update_ai(self.char_x, dt * 1.5, self.walk_speed)
            
            if self.player_hp > 0:
                w_bounce = (abs(math.sin(self.motion_time)) * 1.5) if self.physics.is_grounded else 0
                i_bounce = ((math.sin(current_time * 3.0) * 0.3) + 0.3) if self.physics.is_grounded else 0
                bounce = (w_bounce * self.walk_weight) + (i_bounce * (1.0 - self.walk_weight))
                sway = (math.sin(self.motion_time) * 0.4) * self.walk_weight if self.physics.is_grounded else 0
            else:
                bounce, sway = 0, 0

            foot_tip = self.actor.render(
                screen=self.screen,
                cx=self.char_x + sway,
                base_y=self.base_y - bounce,
                p_time=self.motion_time,
                i_time=current_time * 3.0,
                weight=self.walk_weight,
                jump_y=self.physics.jump_y,
                phys_engine=self.physics,
                is_kick=self.physics.is_kicking,
                kick_t=self.physics.kick_time,
                direction=self.direction,
                p_size=self.pixel_size,
                width=self.width
            )
            
            self.enemy.render(self.screen, current_time, self.pixel_size, self.width)
            
            self.check_combat_collisions()
            
            self.draw_health_bars()
            
            self.effects.update_and_render(self.screen, dt, self.pixel_size, self.width)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = SoftBodyGameLauncher()
    launcher.run()