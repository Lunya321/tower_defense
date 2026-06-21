from models.enemy import Enemy


class HealerEnemy(Enemy):

    def __init__(self, path, tile_size):
        super().__init__(path, tile_size)
        self.type_name = "healer"
        self.speed = 100
        self.hp = 80
        self.reward = 30