from models.tower import Tower
from models.projectiles import Cannonball

class CannonTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.type_name = "cannon"
        self.range = 100
        self.damage = 80
        self.cooldown = 2.0
        self.cost = 100
        self.aoe_radius = 60

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
            self._apply_aoe_damage(enemies)
            return self._create_projectile()

        return None

    def _apply_aoe_damage(self, enemies):
        if not self.target:
            return
        for enemy in enemies:
            if enemy.is_alive:
                distance = self.target.pos.distance_to(enemy.pos)
                if distance <= self.aoe_radius:
                    enemy.take_damage(self.damage)

    def _create_projectile(self):
        return Cannonball(self.pos, self.target, self.damage)