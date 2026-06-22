import pygame

class InputHandler:
    def __init__(self):
        self.held_keys = set()
        self.kick_triggered = False
        self.jump_triggered = False

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:   self.held_keys.add("Left")
            if event.key == pygame.K_RIGHT:  self.held_keys.add("Right")
            if event.key == pygame.K_UP:     self.jump_triggered = True
            if event.key == pygame.K_SPACE:  self.kick_triggered = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:   self.held_keys.discard("Left")
            if event.key == pygame.K_RIGHT:  self.held_keys.discard("Right")

    def is_key_held(self, key): return key in self.held_keys
    def check_kick(self):
        if self.kick_triggered:
            self.kick_triggered = False
            return True
        return False
    def check_jump(self):
        if self.jump_triggered:
            self.jump_triggered = False
            return True
        return False
