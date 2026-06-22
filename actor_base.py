import math

class ActorBase:
    @staticmethod
    def calculate_core(cx, base_y, p_time, i_time, weight, jump_y, phys_engine, is_kick, kick_t):
        kick_factor = math.sin((kick_t / 0.4) * math.pi) if is_kick else 0.0
        
        is_hit = phys_engine.hit_stun_timer > 0 and not phys_engine.is_dead
        hit_ratio = max(0.0, min(1.0, phys_engine.hit_stun_timer / 0.25)) if not phys_engine.is_dead else 0.0
        
        is_dead = phys_engine.is_dead
        angle = phys_engine.ko_angle
        
        walk_cycle_bounce = abs(math.sin(p_time)) * 2.0 if (phys_engine.is_grounded and not is_hit and not is_dead) else 0.0
        
        pelvis_sink = phys_engine.flex_intensity * 4.0
        target_hip_y = base_y - jump_y + walk_cycle_bounce + (pelvis_sink if not is_dead else phys_engine.flex_intensity * 1.5)
        
        chest_lag = phys_engine.chest_spring_y.update(target_hip_y, 0.016)
        head_lag = phys_engine.head_spring_y.update(chest_lag, 0.016)
        
        hit_lean_x = -hit_ratio * 4.0
        target_sway_x = (math.sin(p_time) * 0.5 * weight) + (kick_factor * -3.0) + hit_lean_x
        x_wobble = phys_engine.flesh_wobble_x.update(target_sway_x, 0.016)
        
        vel_impact = phys_engine.v_velocity * 0.01
        squash_y = 1.0 - min(0.25, max(-0.2, vel_impact)) - (hit_ratio * 0.15 if not is_dead else 0)
        stretch_x = 1.0 / squash_y
        
        if is_dead:
            torso_len = 5.0
            neck_len = 11.0
            
            hip_x, hip_y = cx, target_hip_y
            chest_x = cx - math.sin(angle) * torso_len
            chest_y = target_hip_y - math.cos(angle) * torso_len
            
            head_x = cx - math.sin(angle) * neck_len
            head_y = target_hip_y - math.cos(angle) * neck_len
        else:
            hip_x, hip_y = cx, target_hip_y
            chest_x, chest_y = cx + x_wobble, chest_lag - 5
            head_x, head_y = cx + x_wobble * 1.1 + (kick_factor * -0.8), head_lag - 11 + (hit_ratio * 1.5)
        
        return {
            "hip": (hip_x, hip_y), "chest": (chest_x, chest_y), "head": (head_x, head_y),
            "squash_y": squash_y, "stretch_x": stretch_x, "kick_factor": kick_factor,
            "hit_ratio": hit_ratio, "is_dead": is_dead, "ko_angle": angle
        }