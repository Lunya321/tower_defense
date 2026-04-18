from models.map_model import MapModel
from models.wave_manager import WaveManager
from models.tower import Tower
from views.map_renderer import MapRenderer
import pygame

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.map_model = MapModel()
        self.map_renderer = MapRenderer(self.map_model)
        
        self.wave_manager = WaveManager(self.map_model.path, self.map_model.tile_size)
        
        self.enemies = []
        self.towers = []
        self.projectiles = []

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // self.map_model.tile_size
            grid_y = mouse_y // self.map_model.tile_size
            
            if self.map_model.get_tile(grid_x, grid_y) == 0:
                new_tower = Tower(grid_x, grid_y, self.map_model.tile_size)
                self.towers.append(new_tower)

    def update(self, dt):
        new_enemy = self.wave_manager.update(dt)
        if new_enemy:
            self.enemies.append(new_enemy)

        for enemy in self.enemies:
            enemy.update(dt)
            
        for tower in self.towers:
            new_projectile = tower.update(dt, self.enemies)
            if new_projectile:
                self.projectiles.append(new_projectile)

        for proj in self.projectiles:
            proj.update(dt)
        
        self.enemies = [e for e in self.enemies if e.is_alive]
        self.projectiles = [p for p in self.projectiles if p.is_active]

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map_renderer.render(self.screen)
        
        for tower in self.towers:
            pygame.draw.circle(self.screen, (0, 0, 255), (int(tower.pos.x), int(tower.pos.y)), 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(tower.pos.x), int(tower.pos.y)), tower.range, 1)

        for enemy in self.enemies:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(enemy.pos.x), int(enemy.pos.y)), 15)
            
        for proj in self.projectiles:
            pygame.draw.circle(self.screen, (255, 255, 0), (int(proj.pos.x), int(proj.pos.y)), 5)