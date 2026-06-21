import pygame
from models.projectiles import Arrow, SniperArrow, Cannonball, IceProjectile


class Tower:

    def __init__(self, grid_x, grid_y, tile_size):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size
        self.pos = pygame.Vector2(
            grid_x * tile_size + tile_size // 2,
            grid_y * tile_size + tile_size // 2,
        )
        self.range = 150
        self.cooldown = 1.0
        self.timer = 0.0
        self.damage = 20
        self.cost = 100
        self.type_name = "generic"
        self.target = None

    def _find_target(self, enemies):
        for enemy in enemies:
            if enemy.is_alive:
                distance = self.pos.distance_to(enemy.pos)
                if distance <= self.range:
                    return enemy
        return None

    def update(self, dt, enemies):
        if self.timer > 0:
            self.timer -= dt

        if self.target and (
            not self.target.is_alive
            or self.pos.distance_to(self.target.pos) > self.range
        ):
            self.target = None

        if not self.target:
            self.target = self._find_target(enemies)

        if self.target and self.timer <= 0:
            self.timer = self.cooldown
            return self._create_projectile()

        return None

    def _create_projectile(self):
        return Arrow(self.pos, self.target, self.damage)


class ArrowTower(Tower):

    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 160
        self.cooldown = 0.8
        self.damage = 20
        self.cost = 20
        self.type_name = "arrow"

    def _create_projectile(self):
        return Arrow(self.pos, self.target, self.damage)


class CannonTower(Tower):

    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 120
        self.cooldown = 2.0
        self.damage = 50
        self.cost = 45
        self.type_name = "cannon"

    def _create_projectile(self):
        return Cannonball(self.pos, self.target, self.damage)


class IceTower(Tower):

    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 130
        self.cooldown = 1.2
        self.damage = 15
        self.cost = 35
        self.type_name = "ice"

    def _create_projectile(self):
        return IceProjectile(self.pos, self.target, self.damage)


class SniperTower(Tower):

    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 300
        self.cooldown = 3.5
        self.damage = 90
        self.cost = 70
        self.type_name = "sniper"

    def _create_projectile(self):
        return SniperArrow(self.pos, self.target, self.damage)