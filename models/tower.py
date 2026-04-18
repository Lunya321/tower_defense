import pygame

class Tower:
    def __init__(self, grid_x, grid_y, tile_size):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size

        self.pos = pygame.Vector2(
            grid_x * tile_size + tile_size // 2,
            grid_y * tile_size + tile_size // 2 
        )

        self.range = 120
        self.damage = 50
        self.cooldown = 1.0
        self.current_cooldown = 0.0

    def update(self, dt, enemies):
        if self.current_cooldown > 0:
            self.current_cooldown -= dt
            return 
        
        target = self._find_target(enemies)
        if target is not None:
            target.take_damage(self.damage)
            self.current_cooldown = self.cooldown

    def _find_target(self, enemies):
        for enemy in enemies:
            if not enemy.is_alive:
                continue
            
            distance = self.pos.distance_to(enemy.pos)
            if distance <= self.range:
                return enemy
            
        return None