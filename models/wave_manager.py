import random
from models.enemies import BasicEnemy, FastEnemy, TankEnemy, HealerEnemy

class WaveManager:
    def __init__(self, path, tile_size):
        self.path = path
        self.tile_size = tile_size
        self.current_wave = 1
        self.max_waves = 5
        self.level = 1
        self.is_active = False
        self.enemies_queue = []
        
        self.spawn_timer = 0.0
        self.spawn_delay = 1.2
        self.wave_timer = 0.0
        self.time_between_waves = 5.0

    def _start_wave(self):
        self.is_active = True
        self.enemies_queue = self._generate_wave_enemies()
        random.shuffle(self.enemies_queue)
        self.spawn_timer = self.spawn_delay

    def _generate_wave_enemies(self):
        enemies = []
        basic_count = 3 + (self.current_wave * 2) + (self.level * 2)
        
        for _ in range(basic_count):
            enemies.append("basic")
        
        if self.current_wave >= 2 or self.level >= 2:
            fast_count = self.current_wave + self.level
            for _ in range(fast_count):
                enemies.append("fast")
        
        if self.current_wave >= 3 or self.level >= 2:
            tank_count = max(1, self.current_wave - 2 + self.level)
            for _ in range(tank_count):
                enemies.append("tank")
        
        if self.current_wave >= 4 or self.level >= 3:
            healer_count = max(1, self.current_wave - 3 + self.level - 1)
            for _ in range(healer_count):
                enemies.append("healer")
        
        return enemies

    def _create_enemy(self, enemy_type):
        if enemy_type == "basic":
            return BasicEnemy(self.path, self.tile_size)
        elif enemy_type == "fast":
            return FastEnemy(self.path, self.tile_size)
        elif enemy_type == "tank":
            return TankEnemy(self.path, self.tile_size)
        elif enemy_type == "healer":
            return HealerEnemy(self.path, self.tile_size)
        return None

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
                enemy_type = self.enemies_queue.pop(0)
                return self._create_enemy(enemy_type)
        else:
            if active_enemies_count == 0:
                self.is_active = False
                self.current_wave += 1
                
        return None

    def is_level_complete(self):
        return self.current_wave > self.max_waves

    def next_level(self):
        self.level += 1
        self.current_wave = 1
        self.is_active = False
        self.wave_timer = 0.0