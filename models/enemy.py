import pygame

class Enemy:
    def __init__(self, path, tile_size):
        self.path = path
        self.tile_size = tile_size
        
        self.pos = pygame.Vector2(
            path[0][0] * tile_size + tile_size // 2,
            path[0][1] * tile_size + tile_size // 2
        )
        
        self.target_waypoint_index = 1
        self.speed = 100
        self.is_alive = True
        
        self.hp = 100
        self.reward = 15
        self.base_damage = 1
        self.reached_base = False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.is_alive = False

    def update(self, dt):
        if not self.is_alive:
            return

        if self.target_waypoint_index >= len(self.path):
            self.reached_base = True
            self.is_alive = False
            return

        target_tile = self.path[self.target_waypoint_index]
        target_pos = pygame.Vector2(
            target_tile[0] * self.tile_size + self.tile_size // 2,
            target_tile[1] * self.tile_size + self.tile_size // 2
        )

        move_vec = target_pos - self.pos
        distance = move_vec.length()

        if distance <= self.speed * dt:
            self.pos = target_pos
            self.target_waypoint_index += 1
        else:
            self.pos += move_vec.normalize() * self.speed * dt