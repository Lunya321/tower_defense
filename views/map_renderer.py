import pygame
import os

class MapRenderer:
    def __init__(self, screen, map_model, tile_size=40):
        self.screen = screen
        self.map_model = map_model
        self.tile_size = tile_size
        self.textures = {}
        self._load_assets()

    def _load_assets(self):
        base_path = os.path.join("assets", "img", "tiles")
        asset_map = {
            0: "land.png",
            1: "road_5.png",
            2: "road_6.png",
            3: "stone_1.png"
        }

        for tile_id, file_name in asset_map.items():
            path = os.path.join(base_path, file_name)
            if os.path.exists(path):
                raw_img = pygame.image.load(path).convert_alpha()
                self.textures[tile_id] = pygame.transform.smoothscale(
                    raw_img, (self.tile_size, self.tile_size)
                )

    def render(self):
        grid = self.map_model.grid
        for row_idx, row in enumerate(grid):
            for col_idx, tile_id in enumerate(row):
                texture = self.textures.get(tile_id)
                if texture:
                    x = col_idx * self.tile_size
                    y = row_idx * self.tile_size
                    self.screen.blit(texture, (x, y))