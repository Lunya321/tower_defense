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
