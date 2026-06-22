import math

class SoftBodySpring:
    def __init__(self, stiffness, damping):
        self.pos = 0.0
        self.vel = 0.0
        self.stiffness = stiffness  
        self.damping = damping      

    def update(self, target, dt):
        displacement = target - self.pos
        force = displacement * self.stiffness
        self.vel += force * dt
        self.vel -= self.vel * self.damping * dt
        self.pos += self.vel * dt
        return self.pos

class PhysicsEngine:
    def __init__(self, base_y):
        self.base_y = base_y
        self.jump_y = 0.0
        self.v_velocity = 0.0
        self.gravity = 42.0
        self.jump_force = 32.0
        self.is_grounded = True
        
        self.flex_intensity = 0.0
        self.flex_velocity = 0.0
        
        self.kick_time = 0.0
        self.is_kicking = False
        self.kick_duration = 0.4
        
        self.chest_spring_y = SoftBodySpring(stiffness=120.0, damping=8.0)
        self.head_spring_y = SoftBodySpring(stiffness=90.0, damping=7.0)
        self.flesh_wobble_x = SoftBodySpring(stiffness=100.0, damping=6.0)
        
        self.knockback_vx = 0.0   
        self.hit_stun_timer = 0.0 

        self.has_hit_current_attack = False
        self.is_dead = False
        self.ko_angle = 0.0

    def start_jump(self):
        if self.is_grounded and self.hit_stun_timer <= 0:
            self.v_velocity = self.jump_force
            self.is_grounded = False
            self.flex_intensity = 0.0

    def start_kick(self):
        if not self.is_kicking and self.hit_stun_timer <= 0:
            self.is_kicking = True
            self.kick_time = 0.0
            self.has_hit_current_attack = False

    def take_damage(self, attacker_direction):
        self.is_kicking = False  
        self.kick_time = 0.0
        self.hit_stun_timer = 0.25  
        self.knockback_vx = attacker_direction * 45.0
        self.flex_intensity = 1.0

    def update(self, dt):
        if abs(self.knockback_vx) > 0.01:
            self.knockback_vx -= self.knockback_vx * 8.0 * dt
            
        if self.hit_stun_timer > 0:
            self.hit_stun_timer -= dt

        if not self.is_grounded:
            self.v_velocity -= self.gravity * dt
            self.jump_y += self.v_velocity * dt
            if self.jump_y <= 0.0:
                self.jump_y = 0.0
                impact = abs(self.v_velocity)
                self.v_velocity = 0.0
                self.is_grounded = True
                self.flex_intensity = min(1.2, impact * 0.04)
        else:
            spring_k = 140.0
            damp = 10.0
            disp = 0.0 - self.flex_intensity
            self.flex_velocity += disp * spring_k * dt
            self.flex_velocity -= self.flex_velocity * damp * dt
            self.flex_intensity += self.flex_velocity * dt

        kick_dash_offset = 0.0
        if self.is_kicking:
            if self.kick_time < 0.2:
                kick_dash_offset = 35.0 * dt
            self.kick_time += dt
            if self.kick_time >= self.kick_duration:
                self.is_kicking = False
                self.kick_time = 0.0
                
        return kick_dash_offset + (self.knockback_vx * dt)