import os
import pygame


class AssetManager:

    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.towers = {}
        self.enemies = {}
        self._load_assets()

    def _load_assets(self):
        base_path = os.path.join("assets", "images")
        tower_types = ["arrow", "cannon", "slow", "sniper"]
        for t_type in tower_types:
            path = os.path.join(base_path, "towers", f"{t_type}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.towers[t_type] = pygame.transform.scale(
                    img, (self.tile_size, self.tile_size)
                )
        enemy_types = ["basic", "fast", "tank", "healer"]
        for e_type in enemy_types:
            path = os.path.join(base_path, "enemies", f"{e_type}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.enemies[e_type] = pygame.transform.scale(
                    img, (self.tile_size, self.tile_size)
                )