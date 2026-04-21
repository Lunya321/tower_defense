from models.tower import Tower

class CannonTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 100
        self.damage = 80
        self.cooldown = 2.0   
        self.cost = 100