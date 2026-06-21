from models.enemy import Enemy


class TankEnemy(Enemy):

    def __init__(self, path, tile_size):
        super().__init__(path, tile_size)
        self.type_name = "tank"
        self.speed = 50
        self.hp = 300
        self.reward = 40