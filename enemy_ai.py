import random

class EnemyAI:
    @staticmethod
    def process_behavior(actor, player_x, dt, walk_speed, base_y):
        if actor.enemy_hp <= 0:
            actor.ai_state = "KO"
            if not actor.is_dead:
                actor.ko_time += dt
                if actor.ko_time < 0.3:
                    actor.char_x += -actor.direction * 25.0 * dt
                if actor.ko_time >= 0.8:
                    actor.is_dead = True
            return False, 0.0, actor.char_x

        if actor.char_x < player_x:
            actor.direction = 1
        else:
            actor.direction = -1

        distance = abs(actor.char_x - player_x)

        actor.decision_timer -= dt
        if actor.decision_timer <= 0:
            actor.decision_timer = random.uniform(0.2, 0.5)
            if distance > 11:     
                actor.ai_state = "APPROACH"
            elif distance <= 11:  
                actor.ai_state = "KICK" if random.random() < 0.6 else "IDLE"

        is_moving_now = False
        if actor.ai_state == "APPROACH" and not actor.is_kicking:
            is_moving_now = True
            actor.char_x += actor.direction * 12.0 * dt
            actor.motion_time += dt * walk_speed
        elif actor.ai_state == "KICK" and not actor.is_kicking:
            actor.is_kicking = True
            actor.kick_time = 0.0
            actor.ai_state = "IDLE" 

        kick_dash_offset = 0.0
        if actor.is_kicking:
            if actor.kick_time < 0.2:
                kick_dash_offset = 30.0 * dt
            actor.kick_time += dt
            if actor.kick_time >= actor.kick_duration:
                actor.is_kicking = False
                actor.kick_time = 0.0
        actor.char_x += actor.direction * kick_dash_offset

        blend_speed = 8.0 * dt
        if is_moving_now:
            actor.walk_weight = min(1.0, actor.walk_weight + blend_speed)
        else:
            actor.walk_weight = max(0.0, actor.walk_weight - blend_speed)
            actor.motion_time += dt * walk_speed * actor.walk_weight

        return actor.is_kicking, actor.kick_time, actor.char_x
