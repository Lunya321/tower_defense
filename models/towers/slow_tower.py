from models.tower import Tower

class SlowTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 90
        self.damage = 5
        self.cooldown = 1.0
        self.cost = 75