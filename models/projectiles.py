import pygame

class Projectile:
    def __init__(self, start_pos, target_enemy, damage, speed=300):
        self.pos = pygame.Vector2(start_pos)
        self.target = target_enemy
        self.damage = damage
        self.speed = speed
        self.is_active = True

    def update(self, dt):
        if not self.target.is_alive:
            self.is_active = False
            return

        move_vec = self.target.pos - self.pos
        distance = move_vec.length()

        if distance <= self.speed * dt:
            self.target.take_damage(self.damage)
            self.is_active = False
        else:
            self.pos += move_vec.normalize() * self.speed * dt