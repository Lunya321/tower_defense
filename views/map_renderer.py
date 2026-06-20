import pygame
import os

class MapRenderer:
    def __init__(self, screen, map_model, tile_size=40):
        self.screen = screen
        self.map_model = map_model
        self.tile_size = tile_size
        self.textures = {}
        self._load_tiles()

    def _load_tiles(self):
        base_path = os.path.join("assets", "images", "tiles")
        scale_size = (self.tile_size, self.tile_size)
        
        tile_files = {
            "grass_1": "grass_1.png",
            "grass_2": "grass_2.png",
            "grass_3": "grass_3.png",
            "grass_4": "grass_4.png",
            "grass_flower": "grass_flower.png",
            "grass_bush": "grass_bush.png",
            "road_h": "road_h.png",
            "road_v": "road_v.png",
            "road_rb": "road_rb.png",
            "road_lb": "road_lb.png",
            "road_rt": "road_rt.png",
            "road_lt": "road_lt.png"
        }
        
        for key, filename in tile_files.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                self.textures[key] = pygame.transform.scale(img, scale_size)
            else:
                fallback = pygame.Surface(scale_size)
                fallback.fill((34, 139, 34) if "grass" in key else (139, 69, 19))
                self.textures[key] = fallback

    def _get_grass_variant(self, x, y):
        decor_val = (x * 73 + y * 37) % 100
        if decor_val < 3:
            return self.textures["grass_flower"]
        elif decor_val < 6:
            return self.textures["grass_bush"]
            
        grass_val = (x * 101 + y * 13) % 4
        return self.textures[f"grass_{grass_val + 1}"]

    def _get_path_texture_key(self, x, y, grid):
        height, width = len(grid), len(grid[0])
        top = y > 0 and grid[y-1][x] == 1
        bottom = y < height - 1 and grid[y+1][x] == 1
        left = x > 0 and grid[y][x-1] == 1
        right = x < width - 1 and grid[y][x+1] == 1

        if top and bottom: return "road_v"
        if left and right: return "road_h"
        if bottom and right: return "road_rb"
        if bottom and left: return "road_lb"
        if top and right: return "road_rt"
        if top and left: return "road_lt"
        return "road_h"

    def render(self):
        grid = self.map_model.grid
        for y, row in enumerate(grid):
            for x, tile_id in enumerate(row):
                pos = (x * self.tile_size, y * self.tile_size)
                
                grass_tile = self._get_grass_variant(x, y)
                self.screen.blit(grass_tile, pos)
                
                if tile_id == 1:
                    key = self._get_path_texture_key(x, y, grid)
                    self.screen.blit(self.textures[key], pos)