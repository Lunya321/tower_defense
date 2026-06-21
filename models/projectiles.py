import math
import pygame
from algorithms.collision import check_circle_collision

class Projectile:
    def __init__(self, start_pos, target, damage, speed, type_name):
        self.pos = pygame.Vector2(start_pos)
        self.target = target
        self.target_pos = (
            pygame.Vector2(target.pos) if target else pygame.Vector2(start_pos)
        )
        self.damage = damage
        self.speed = speed
        self.type_name = type_name
        self.is_active = True
        self.angle = 0
        self.hit_radius = 10

    def update(self, dt):
        if not self.is_active:
            return

        if self.target and self.target.is_alive:
            self.target_pos = pygame.Vector2(self.target.pos)

        direction = self.target_pos - self.pos
        distance = direction.length()

        if distance > 0:
            self.angle = math.degrees(math.atan2(-direction.y, direction.x))

        if distance <= self.speed * dt:
            self.pos = self.target_pos
            self.check_collision()
        else:
            self.pos += direction.normalize() * self.speed * dt

    def check_collision(self):
        if self.target and self.target.is_alive:
            if check_circle_collision(self.pos, self.target.pos, self.hit_radius, 15):
                self.hit_target()
        else:
            self.is_active = False

    def hit_target(self):
        self.is_active = False
        if self.target and self.target.is_alive:
            self.target.take_damage(self.damage)

class Arrow(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(
            start_pos, target, damage=damage, speed=450, type_name="arrow"
        )
        self.hit_radius = 8

class SniperArrow(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(
            start_pos, target, damage=damage, speed=600, type_name="snip"
        )
        self.hit_radius = 6

class Cannonball(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(
            start_pos, target, damage=damage, speed=250, type_name="cannonball"
        )
        self.hit_radius = 12

class IceProjectile(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(
            start_pos, target, damage=damage, speed=350, type_name="ice"
        )
        self.hit_radius = 10