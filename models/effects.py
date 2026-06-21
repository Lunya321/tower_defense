import pygame


class VisualEffect:

    def __init__(self, pos, type_name, duration=0.25):
        self.pos = pygame.Vector2(pos)
        self.type_name = type_name
        self.duration = duration
        self.elapsed_time = 0
        self.is_active = True

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.is_active = False