import math
import vector
from enemy_ai import EnemyAI

class ProceduralEnemy:
    def __init__(self, base_y):
        self.color_skin = (255, 209, 169)
        self.color_hair = (45, 55, 72)         
        self.color_headband = (229, 62, 62)     
        self.color_gi_top = (247, 250, 252)     
        self.color_gi_bot = (237, 242, 247)     
        self.color_belt = (26, 32, 44)          
        self.color_glove = (197, 48, 48)        
        self.color_limb_back = (160, 174, 192)  

        self.base_y = base_y
        self.char_x = 65.0  
        self.direction = -1  
        
        self.walk_weight = 0.0
        self.motion_time = 0.0
        self.kick_time = 0.0
        self.is_kicking = False
        self.kick_duration = 0.4
        
        self.decision_timer = 0.0
        self.ai_state = "IDLE"  
        
        self.enemy_hp = 100
        self.ko_time = 0.0
        self.is_dead = False

    def update_ai(self, player_x, dt, walk_speed):
        return EnemyAI.process_behavior(self, player_x, dt, walk_speed, self.base_y)

    def render(self, screen, current_time, p_size, w_pixels):
        floor_y = self.base_y + 10.5
        kick_factor = math.sin((self.kick_time / 0.4) * math.pi) if self.is_kicking else 0.0
        
        ko_offset_y = 0.0
        ko_rot_y = 0.0
        ko_squash_y = 1.0
        ko_stretch_x = 1.0
        
        if self.ai_state == "KO":
            if self.ko_time < 0.4:
                ko_offset_y = -math.sin((self.ko_time / 0.4) * math.pi) * 8.0
                ko_rot_y = (self.ko_time / 0.4) * 4.0
            else:
                progress = min(1.0, (self.ko_time - 0.4) / 0.4)
                ko_offset_y = 10.0 * progress
                ko_rot_y = 4.0 + progress * 6.0
                ko_squash_y = max(0.2, 1.0 - progress * 0.7)
                ko_stretch_x = 1.0 / ko_squash_y
        
        walk_bounce = math.sin(self.motion_time) * 2.0 if (self.is_kicking or self.walk_weight > 0) else 0.0
        target_hip_y = self.base_y + abs(walk_bounce) + ko_offset_y
        
        cx = self.char_x
        hip_x, hip_y = cx, target_hip_y
        
        chest_x, chest_y = cx + (kick_factor * -2.5) - (ko_rot_y * 1.5), target_hip_y - 5 + (ko_rot_y * 0.8)
        head_x, head_y = cx + (kick_factor * -3.3) - (ko_rot_y * 3.0), target_hip_y - 11 + (ko_rot_y * 1.5)

        def draw_ryu_upper_body():
            vector.draw_blob(screen, cx, head_x, head_y - 0.5, 2.4 * ko_stretch_x, 2.4 * ko_squash_y, self.color_skin, p_size, self.direction, w_pixels)
            vector.draw_blob(screen, cx, head_x, head_y - 2.0, 2.6, 1.2 * ko_squash_y, self.color_hair, p_size, self.direction, w_pixels)
            
            vector.draw_pixel_line(screen, cx, head_x - 1.5, head_y - 1, head_x + 1.5, head_y - 1, self.color_headband, p_size, self.direction, w_pixels)
            band_flow = kick_factor * -2.0 + math.sin(current_time * 4) * 0.4 + (self.ko_time * 3.0 if self.ai_state == "KO" else 0)
            vector.draw_pixel_line(screen, cx, head_x - 1.5, head_y - 1, head_x - 3.5 + band_flow, head_y - 0.2, self.color_headband, p_size, self.direction, w_pixels)
            
            vector.draw_pixel_line(screen, cx, head_x, head_y + 1, chest_x, chest_y - 3, self.color_skin, p_size, self.direction, w_pixels)
            vector.draw_blob(screen, cx, chest_x, chest_y, 3.4 * ko_stretch_x, 3.0 * ko_squash_y, self.color_gi_top, p_size, self.direction, w_pixels)
            
            local_ox = (chest_x + 0.5) - cx
            flipped_bx = cx + (local_ox * self.direction)
            vector.draw_pixel_block(screen, flipped_bx, chest_y - 1.5, self.color_skin, p_size, self.direction, w_pixels) 
            
            vector.draw_blob(screen, cx, hip_x, hip_y - 1, 3.0 * ko_stretch_x, 2.0 * ko_squash_y, self.color_gi_bot, p_size, self.direction, w_pixels)
            vector.draw_pixel_line(screen, cx, hip_x - 2.5, hip_y - 2, hip_x + 2.5, hip_y - 2, self.color_belt, p_size, self.direction, w_pixels)

        def render_ryu_leg(phase, color, is_left):
            h_x, h_y = hip_x, hip_y + 1
            if self.ai_state == "KO":
                f_x = h_x - 4.0 + (phase * 0.1) - (self.ko_time * 2.0)
                f_y = h_y + 2.0 - (ko_offset_y * 0.5)
                if f_y > floor_y: f_y = floor_y
                k_x = (h_x + f_x) / 2 - 1.0
                k_y = (h_y + f_y) / 2 + 1.0
            elif is_left and kick_factor > 0.001:
                f_x = h_x + 3.0 + (kick_factor * 8.5)
                f_y = h_y - 2.5 - (kick_factor * 2.0)
                k_x = (h_x + f_x) / 2 + 0.1 + ((1.0 - kick_factor) * 0.8)
                k_y = (h_y + f_y) / 2 - 0.4
            elif not is_left and kick_factor > 0.001:
                f_x = h_x - 2.5 - (kick_factor * 0.8)
                f_y = floor_y
                k_x = (h_x + f_x) / 2 + 1.0 - (kick_factor * 0.6)
                k_y = (h_y + f_y) / 2 + 0.8
            else:
                swing = (math.sin(phase) * 4.8 * self.walk_weight) + ((-0.8 if is_left else 0.8) * (1.0 - self.walk_weight))
                lift = max(0, math.cos(phase)) * 2.5 * self.walk_weight
                f_x = h_x + swing
                f_y = floor_y - lift
                k_offset = ((1.2 + math.sin(phase) * 1.2) * self.walk_weight) + (0.8 * (1.0 - self.walk_weight))
                k_x = (h_x + f_x) / 2 + k_offset
                k_y = (h_y + f_y) / 2 + 0.3

            vector.draw_pixel_line(screen, cx, h_x, h_y, k_x, k_y, color, p_size, self.direction, w_pixels)
            vector.draw_pixel_line(screen, cx, k_x, k_y, f_x, f_y, color, p_size, self.direction, w_pixels)
            vector.draw_blob(screen, cx, (h_x+k_x)/2, (h_y+k_y)/2, 2.0 * ko_stretch_x, 1.8 * ko_squash_y, color, p_size, self.direction, w_pixels)
            vector.draw_blob(screen, cx, (k_x+f_x)/2, (k_y+f_y)/2, 1.8 * ko_stretch_x, 1.6 * ko_squash_y, color, p_size, self.direction, w_pixels)
            
            vector.draw_blob(screen, cx, f_x, f_y, 1.5 * ko_stretch_x, 1.0 * ko_squash_y, self.color_skin, p_size, self.direction, w_pixels)
            f_edge = 2.0 if (is_left and kick_factor > 0.4 and self.ai_state != "KO") else 1.2
            
            local_fx = (f_x + f_edge) - cx
            flipped_fx = cx + (local_fx * self.direction)
            vector.draw_pixel_block(screen, flipped_fx, f_y, self.color_skin, p_size, self.direction, w_pixels)

        def render_ryu_arm(phase, color, glove_color):
            s_x, s_y = chest_x, chest_y - 2
            
            if self.ai_state == "KO":
                arm_swing = -5.0 + math.sin(self.ko_time * 10) * 1.5
                e_x = s_x + arm_swing
                e_y = s_y - 4.0
                ha_x = e_x - 2.0
                ha_y = e_y - 3.0
            else:
                arm_swing = (math.sin(phase + math.pi) * 3.2 * self.walk_weight) + (kick_factor * (3.0 if color == self.color_gi_top else -4.0))
                e_x = s_x + arm_swing
                e_y = s_y + 3.2 - (kick_factor * 2.0)
                ha_x = e_x + (math.sin(phase + math.pi + 0.2) * 2.2 * self.walk_weight) + (kick_factor * 1.5)
                ha_y = e_y + 2.2
            
            vector.draw_blob(screen, cx, s_x, s_y, 1.6 * ko_stretch_x, 1.4 * ko_squash_y, color, p_size, self.direction, w_pixels)
            vector.draw_pixel_line(screen, cx, s_x, s_y + 0.5, e_x, e_y, self.color_skin, p_size, self.direction, w_pixels)
            vector.draw_pixel_line(screen, cx, e_x, e_y, ha_x, ha_y, self.color_skin, p_size, self.direction, w_pixels)
            vector.draw_blob(screen, cx, (s_x+e_x)/2, (s_y+e_y)/2, 1.3 * ko_stretch_x, 1.1 * ko_squash_y, self.color_skin, p_size, self.direction, w_pixels)
            vector.draw_blob(screen, cx, ha_x, ha_y, 1.2 * ko_stretch_x, 1.2 * ko_squash_y, glove_color, p_size, self.direction, w_pixels)

        r_phase = self.motion_time + math.pi
        render_ryu_arm(r_phase, self.color_limb_back, self.color_limb_back)
        render_ryu_leg(r_phase, self.color_limb_back, is_left=False)
        
        draw_ryu_upper_body()
        
        render_ryu_leg(self.motion_time, self.color_gi_top, is_left=True)
        render_ryu_arm(self.motion_time, self.color_gi_top, self.color_glove)
