from models.enemy import Enemy

class WaveManager:
    def __init__(self, path, tile_size):
        self.path = path
        self.tile_size = tile_size
        
        self.current_wave = 1
        self.is_active = False
        self.enemies_queue = []
        
        self.spawn_timer = 0.0
        self.spawn_delay = 1.2
        self.wave_timer = 0.0
        self.time_between_waves = 5.0

    def _start_wave(self):
        self.is_active = True
        enemy_count = 3 + (self.current_wave * 2)
        self.enemies_queue = ["basic"] * enemy_count
        self.spawn_timer = self.spawn_delay 

    def update(self, dt, active_enemies_count):
        if not self.is_active:
            self.wave_timer += dt
            if self.wave_timer >= self.time_between_waves:
                self.wave_timer = 0.0
                self._start_wave()
            return None

        if self.enemies_queue:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_timer = 0.0
                self.enemies_queue.pop()
                return Enemy(self.path, self.tile_size)
        else:
            if active_enemies_count == 0:
                self.is_active = False
                self.current_wave += 1
                
        return None