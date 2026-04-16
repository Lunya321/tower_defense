from models.map_model import MapModel
from models.enemy import Enemy
from views.map_renderer import MapRenderer
import pygame

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.map_model = MapModel()
        self.map_renderer = MapRenderer(self.map_model)
        
        self.enemies = [Enemy(self.map_model.path, self.map_model.tile_size)]

    def handle_input(self, event):
        pass

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)
        
        self.enemies = [e for e in self.enemies if e.is_alive]

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map_renderer.render(self.screen)
        
        for enemy in self.enemies:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(enemy.pos.x), int(enemy.pos.y)), 15)