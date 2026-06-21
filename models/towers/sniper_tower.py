from models.tower import Tower
from models.projectiles import SniperArrow

class SniperTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.type_name = "sniper"
        self.range = 250
        self.damage = 150
        self.cooldown = 3.0
        self.cost = 150

    def _find_target(self, enemies):
        enemies_in_range = []
        for enemy in enemies:
            if enemy.is_alive:
                distance = self.pos.distance_to(enemy.pos)
                if distance <= self.range:
                    enemies_in_range.append(enemy)

        if not enemies_in_range:
            return None

        enemies_in_range.sort(key=lambda e: e.hp, reverse=True)
        return enemies_in_range[0]

    def _create_projectile(self):
        return SniperArrow(self.pos, self.target, self.damage)