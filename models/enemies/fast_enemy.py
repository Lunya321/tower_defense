from models.enemy import Enemy

class FastEnemy(Enemy):
    def __init__(self, path, tile_size):
        super().__init__(path, tile_size)
        self.type_name = "fast"
        self.speed = 160
        self.base_speed = 160
        self.hp = 60
        self.max_hp = 60
        self.reward = 10