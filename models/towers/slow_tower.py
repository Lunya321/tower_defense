from models.tower import Tower
from models.projectiles import IceProjectile

class SlowTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.type_name = "slow"
        self.range = 90
        self.damage = 5
        self.cooldown = 1.0
        self.cost = 75

    def _create_projectile(self):
        return IceProjectile(self.pos, self.target, self.damage)