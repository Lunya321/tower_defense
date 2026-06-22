from models.enemy import Enemy

class TankEnemy(Enemy):
    def __init__(self, path, tile_size):
        super().__init__(path, tile_size)
        self.type_name = "tank"
        self.speed = 50
        self.base_speed = 50
        self.hp = 300
        self.max_hp = 300
        self.reward = 10
        self.base_damage = 5