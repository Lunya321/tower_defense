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
        
        self.textures[0] = self._load_and_scale(os.path.join(base_path, "land.png"))
        
        self.textures["road_v"] = self._load_and_scale(os.path.join(base_path, "road_5.png"))
        self.textures["road_h"] = self._load_and_scale(os.path.join(base_path, "road_6.png"))
        self.textures["road_rb"] = self._load_and_scale(os.path.join(base_path, "road_1.png"))
        self.textures["road_lb"] = self._load_and_scale(os.path.join(base_path, "road_2.png"))
        self.textures["road_rt"] = self._load_and_scale(os.path.join(base_path, "road_3.png"))
        self.textures["road_lt"] = self._load_and_scale(os.path.join(base_path, "road_4.png"))

    def _load_and_scale(self, path):
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, (self.tile_size, self.tile_size))
        return pygame.Surface((self.tile_size, self.tile_size))

    def _get_path_texture(self, x, y, grid):
        height = len(grid)
        width = len(grid[0])
        
        top = y > 0 and grid[y-1][x] == 1
        bottom = y < height - 1 and grid[y+1][x] == 1
        left = x > 0 and grid[y][x-1] == 1
        right = x < width - 1 and grid[y][x+1] == 1

        if top and bottom: return self.textures["road_v"]
        if left and right: return self.textures["road_h"]
        if bottom and right: return self.textures["road_rb"]
        if bottom and left: return self.textures["road_lb"]
        if top and right: return self.textures["road_rt"]
        if top and left: return self.textures["road_lt"]
        
        return self.textures["road_h"]

    def render(self):
        grid = self.map_model.grid
        for y, row in enumerate(grid):
            for x, tile_id in enumerate(row):
                pos = (x * self.tile_size, y * self.tile_size)
                
                self.screen.blit(self.textures[0], pos)
                
                if tile_id == 1:
                    texture = self._get_path_texture(x, y, grid)
                    self.screen.blit(texture, pos)