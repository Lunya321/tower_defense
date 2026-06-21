from models.enemy import Enemy

class BasicEnemy(Enemy):
    def __init__(self, path, tile_size):
        super().__init__(path, tile_size)
        self.type_name = "basic"
        self.speed = 90
        self.base_speed = 90
        self.hp = 100
        self.max_hp = 100
        self.reward = 15