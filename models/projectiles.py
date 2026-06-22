import math
import pygame

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
            self.hit_target()
        else:
            self.pos += direction.normalize() * self.speed * dt

    def hit_target(self):
        self.is_active = False
        if self.target and self.target.is_alive:
            self.target.take_damage(self.damage)

class Arrow(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(start_pos, target, damage=damage, speed=450, type_name="arrow")

class SniperArrow(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(start_pos, target, damage=damage, speed=600, type_name="snip")

class Cannonball(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(start_pos, target, damage=damage, speed=250, type_name="cannonball")
        self.effect_type = "cannonball"

class IceProjectile(Projectile):
    def __init__(self, start_pos, target, damage):
        super().__init__(start_pos, target, damage=damage, speed=350, type_name="ice")
        self.slow_factor = 0.5
        self.slow_duration = 2.0
        self.effect_type = "ice"

    def hit_target(self):
        self.is_active = False
        if self.target and self.target.is_alive:
            self.target.take_damage(self.damage)
            if hasattr(self.target, 'apply_slow'):
                self.target.apply_slow(self.slow_factor, self.slow_duration)