from models.tower import Tower

class SniperTower(Tower):
    def __init__(self, grid_x, grid_y, tile_size):
        super().__init__(grid_x, grid_y, tile_size)
        self.range = 250      
        self.damage = 150
        self.cooldown = 3.0
        self.cost = 150