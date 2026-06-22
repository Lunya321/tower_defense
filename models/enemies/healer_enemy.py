from models.enemy import Enemy

class HealerEnemy(Enemy):
    def __init__(self, path, tile_size):
        super().__init__(path, tile_size)
        self.type_name = "healer"
        self.speed = 80
        self.base_speed = 80
        self.hp = 120
        self.max_hp = 120