import random
import pygame

class PixelParticle:
    def __init__(self, x, y, vx, vy, color, duration, gravity=15.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = duration
        self.max_life = duration
        self.gravity = gravity

    def update(self, dt):
        """Applies physics movement and counts down particle lifespan."""
        self.vy += self.gravity * dt  # Gravity pulling the particle down
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        return self.life > 0

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_dust(self, x, y):
        """Spawns a dust puff burst when a character lands on the ground."""
        for _ in range(8):
            vx = random.uniform(-12, 12)
            vy = random.uniform(-8, -2)
            duration = random.uniform(0.2, 0.4)
            color = random.choice([(113, 128, 150), (160, 174, 192), (203, 213, 224)])
            self.particles.append(PixelParticle(x, y, vx, vy, color, duration, gravity=8.0))

    def spawn_kick_spark(self, x, y, direction):
        """Spawns sharp energy fire sparks at the tip of the foot during a kick."""
        for _ in range(6):
            vx = direction * random.uniform(20, 45)
            vy = random.uniform(-15, 15)
            duration = random.uniform(0.15, 0.3)
            color = random.choice([(255, 235, 59), (255, 152, 0), (255, 255, 255)])
            self.particles.append(PixelParticle(x, y, vx, vy, color, duration, gravity=25.0))

    def update_and_render(self, screen, dt, p_size, width):
        """Updates physics trajectories and renders active particles to the screen."""
        active_particles = []
        for p in self.particles:
            if p.update(dt):
                active_particles.append(p)
                
                px = int(round(p.x)) * p_size
                py = int(round(p.y)) * p_size
                if px < 0: px += width
                elif px >= width: px -= width
                
                pygame.draw.rect(screen, p.color, (px, py, p_size, p_size))
                
        self.particles = active_particles