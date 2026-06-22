import math
import vector

class ActorLimbs:
    @staticmethod
    def render_leg(screen, cx, hip_x, hip_y, floor_y, jump_y, phase, color, skin_color, gi_color, is_left, kick_factor, p_size, direction, width):
        """Draws the muscular legs cleanly at their correct grounded positions."""
        if is_left and kick_factor > 0.001:  # Extended attack kick
            f_x = hip_x + 3.0 + (kick_factor * 8.5)
            f_y = hip_y - 2.5 - (kick_factor * 2.0)
            k_x = (hip_x + f_x) / 2 + 0.1 + ((1.0 - kick_factor) * 0.8)
            k_y = (hip_y + f_y) / 2 - 0.4
        elif not is_left and kick_factor > 0.001:  # Grounded support leg
            f_x = hip_x - 2.5 - (kick_factor * 0.8)
            f_y = floor_y if jump_y <= 0.1 else hip_y + 8.5
            k_x = (hip_x + f_x) / 2 + 1.0 - (kick_factor * 0.6)
            k_y = (hip_y + f_y) / 2 + 0.8
        else:  # Standard Idle / Locomotion loops
            if jump_y > 0.1:
                swing, lift = (-1.2 if is_left else 1.2), -1.0
                f_y = hip_y + 9.5 - lift
            else:
                swing = (math.sin(phase) * 4.8)
                lift = max(0, math.cos(phase)) * 2.5
                f_y = floor_y - lift
            f_x = hip_x + swing
            k_x = (hip_x + f_x) / 2 + 0.8
            k_y = (hip_y + f_y) / 2 + 0.3

        vector.draw_pixel_line(screen, cx, hip_x, hip_y, k_x, k_y, color, p_size, direction, width)
        vector.draw_pixel_line(screen, cx, k_x, k_y, f_x, f_y, color, p_size, direction, width)
        
        thigh_mid_y = (hip_y + k_y) / 2
        calf_mid_y = (k_y + f_y) / 2
        
        vector.draw_blob(screen, cx, (hip_x + k_x) / 2, thigh_mid_y, 2.0, 1.8, color, p_size, direction, width)
        vector.draw_blob(screen, cx, (k_x + f_x) / 2, calf_mid_y, 1.8, 1.6, color, p_size, direction, width)
        vector.draw_blob(screen, cx, k_x, k_y, 1.5, 1.4, color, p_size, direction, width) # Knee volume block
        
        vector.draw_blob(screen, cx, f_x, f_y, 1.5, 1.0, skin_color, p_size, direction, width)
        f_edge = 2.0 if (is_left and kick_factor > 0.4) else 1.2
        vector.draw_pixel_block(screen, f_x + f_edge, f_y, skin_color, p_size, direction, width)
        
        return f_x, f_y

    @staticmethod
    def render_arm(screen, cx, chest_x, chest_y, phase, color, skin_color, glove_color, kick_factor, p_size, direction, width):
        """Draws muscular arms with tattered gi sleeves and combat gloves."""
        s_x, s_y = chest_x, chest_y - 2
        
        is_front_arm = (color != glove_color)
        arm_multiplier = 3.0 if is_front_arm else -4.0
        arm_swing = (math.sin(phase + math.pi) * 3.2) + (kick_factor * arm_multiplier)
        
        e_x = s_x + arm_swing
        e_y = s_y + 3.2 + abs(math.sin(phase)) * 0.4 - (kick_factor * 2.0)
        
        ha_x = e_x + (math.sin(phase + math.pi + 0.2) * 2.2) + (kick_factor * 1.5)
        ha_y = e_y + 2.2
        
        vector.draw_blob(screen, cx, s_x, s_y, 1.6, 1.4, color, p_size, direction, width)
        vector.draw_pixel_line(screen, cx, s_x, s_y + 0.5, e_x, e_y, skin_color, p_size, direction, width)
        vector.draw_pixel_line(screen, cx, e_x, e_y, ha_x, ha_y, skin_color, p_size, direction, width)
        
        vector.draw_blob(screen, cx, (s_x+e_x)/2, (s_y+e_y)/2, 1.3, 1.1, skin_color, p_size, direction, width)
        vector.draw_blob(screen, cx, e_x, e_y, 1.0, 1.0, skin_color, p_size, direction, width)
        vector.draw_blob(screen, cx, ha_x, ha_y, 1.2, 1.2, glove_color, p_size, direction, width)
        vector.draw_pixel_block(screen, ha_x + 0.5, ha_y + 0.5, skin_color, p_size, direction, width)
