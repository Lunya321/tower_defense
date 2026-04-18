from models.enemy import Enemy

class WaveManager:
    def __init__(self, path, tile_size):
        self.path = path
        self.tile_size = tile_size
        
        self.spawn_timer = 0.0
        self.spawn_interval = 1.5
        self.enemies_to_spawn = 10

    def update(self, dt):
        if self.enemies_to_spawn <= 0:
            return None

        self.spawn_timer -= dt
        
        if self.spawn_timer <= 0:
            new_enemy = Enemy(self.path, self.tile_size)
            
            self.spawn_timer = self.spawn_interval
            self.enemies_to_spawn -= 1
            
            return new_enemy
            
        return None