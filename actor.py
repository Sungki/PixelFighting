import math
import vector
from actor_base import ActorBase
from actor_limbs import ActorLimbs

class ProceduralActor:
    def __init__(self):
        self.color_skin = (255, 209, 169)       
        self.color_hair = (255, 235, 59)        
        self.color_gi_top = (229, 62, 62)       
        self.color_gi_bot = (197, 48, 48)       
        self.color_belt = (45, 55, 72)          
        self.color_glove = (74, 85, 104)        
        self.color_limb_back = (155, 44, 44)    

    def render(self, screen, cx, base_y, p_time, i_time, weight, jump_y, phys_engine, is_kick, kick_t, direction, p_size, width):
        floor_y = base_y + 10.5
        
        core = ActorBase.calculate_core(cx, base_y, p_time, i_time, weight, jump_y, phys_engine, is_kick, kick_t)
        
        hip_x, hip_y = core["hip"]
        chest_x, chest_y = core["chest"]
        head_x, head_y = core["head"]
        kf = core["kick_factor"]
        
        def draw_ken_upper_body():
            vector.draw_blob(screen, cx, head_x - 1, head_y, 2.5, 3.0, self.color_hair, p_size, direction, width) 
            vector.draw_blob(screen, cx, head_x, head_y - 0.5, 2.4 * core["stretch_x"], 2.4 * core["squash_y"], self.color_skin, p_size, direction, width) 
            vector.draw_blob(screen, cx, head_x, head_y - 2.0, 2.6, 1.2, self.color_hair, p_size, direction, width) 
            
            local_hx = (head_x + 1.2) - cx
            flipped_hx = cx + (local_hx * direction)
            vector.draw_pixel_block(screen, flipped_hx, head_y - 1, self.color_hair, p_size, direction, width) 
            
            vector.draw_pixel_line(screen, cx, head_x, head_y + 1, chest_x, chest_y - 3, self.color_skin, p_size, direction, width)
            vector.draw_blob(screen, cx, chest_x, chest_y, 3.4 * core["stretch_x"], 3.0 * core["squash_y"], self.color_gi_top, p_size, direction, width)
            
            local_cx1 = (chest_x + 0.5) - cx
            flipped_cx1 = cx + (local_cx1 * direction)
            vector.draw_pixel_block(screen, flipped_cx1, chest_y - 1.5, self.color_skin, p_size, direction, width)
            
            local_cx2 = (chest_x + 1.0) - cx
            flipped_cx2 = cx + (local_cx2 * direction)
            vector.draw_pixel_block(screen, flipped_cx2, chest_y - 2.0, self.color_skin, p_size, direction, width)
            
            vector.draw_blob(screen, cx, hip_x, hip_y - 1, 3.0, 2.0, self.color_gi_bot, p_size, direction, width)
            
            vector.draw_pixel_line(screen, cx, hip_x - 2.5, hip_y - 2, hip_x + 2.5, hip_y - 2, self.color_belt, p_size, direction, width) 
            
            belt_flow = kf * 2.0 + math.sin(i_time * 2) * 0.5
            vector.draw_pixel_line(screen, cx, hip_x + 0.5, hip_y - 2, hip_x + 1.5 + belt_flow, hip_y + 0.5, self.color_belt, p_size, direction, width)

        r_phase = p_time + math.pi
        
        ActorLimbs.render_arm(screen, cx, chest_x, chest_y, r_phase, self.color_limb_back, self.color_skin, self.color_limb_back, kf, p_size, direction, width)
        ActorLimbs.render_leg(screen, cx, hip_x, hip_y, floor_y, jump_y, r_phase, self.color_limb_back, self.color_skin, self.color_gi_top, False, kf, p_size, direction, width)
        
        draw_ken_upper_body()
        
        fx, fy = ActorLimbs.render_leg(screen, cx, hip_x, hip_y, floor_y, jump_y, p_time, self.color_gi_top, self.color_skin, self.color_gi_top, True, kf, p_size, direction, width)
        ActorLimbs.render_arm(screen, cx, chest_x, chest_y, p_time, self.color_gi_top, self.color_skin, self.color_glove, kf, p_size, direction, width)
        
        actual_foot_x = cx + ((fx - cx) * direction)
        return actual_foot_x, fy
