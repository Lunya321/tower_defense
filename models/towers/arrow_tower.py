from models.tower import Tower

class ArrowTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 120
        self.damage = 20
        self.cooldown = 0.5   
        self.cost = 50