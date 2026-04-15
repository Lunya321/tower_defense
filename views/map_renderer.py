import pygame

class MapRenderer:
    def __init__(self, map_model):
        self.map_model = map_model
        self.COLOR_GRASS = (34, 139, 34)
        self.COLOR_PATH = (210, 180, 140)
        self.COLOR_GRID = (0, 0, 0)

    def render(self, surface):
        for y in range(self.map_model.height):
            for x in range(self.map_model.width):
                tile = self.map_model.get_tile(x, y)
                
                rect = pygame.Rect(
                    x * self.map_model.tile_size,
                    y * self.map_model.tile_size,
                    self.map_model.tile_size,
                    self.map_model.tile_size
                )

                if tile == 0:
                    pygame.draw.rect(surface, self.COLOR_GRASS, rect)
                elif tile == 1:
                    pygame.draw.rect(surface, self.COLOR_PATH, rect)

                pygame.draw.rect(surface, self.COLOR_GRID, rect, 1)