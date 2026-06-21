import pygame
from models.map_model import MapModel
from models.wave_manager import WaveManager
from models.towers import ArrowTower
from views.map_renderer import MapRenderer
from views.hud_view import HudView
from views.asset_manager import AssetManager
from views.game_view import GameView
from algorithms.spatial_hash import SpatialHash


class GameController:

    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.map_model = MapModel()
        self.asset_manager.tile_size = self.map_model.tile_size
        self.map_renderer = MapRenderer(self.screen, self.map_model)
        self.hud_view = HudView()
        self.game_view = GameView(self.screen, self.asset_manager)
        self.wave_manager = WaveManager(
            self.map_model.path, self.map_model.tile_size
        )
        self.spatial_hash = SpatialHash(cell_size=120)
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.money = 100
        self.base_hp = 20

    def start_next_level(self):
        self.map_model = MapModel()
        self.map_renderer = MapRenderer(self.screen, self.map_model)
        self.wave_manager = WaveManager(
            self.map_model.path, self.map_model.tile_size
        )
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.money += 50

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // self.map_model.tile_size
            grid_y = mouse_y // self.map_model.tile_size
            if self.map_model.get_tile(grid_x, grid_y) == 0:
                temp_tower = ArrowTower(
                    grid_x, grid_y, self.map_model.tile_size
                )
                if self.money >= temp_tower.cost:
                    self.money -= temp_tower.cost
                    self.towers.append(temp_tower)

    def update(self, dt):
        if self.base_hp <= 0:
            return
        if self.wave_manager.current_wave > 5 and len(self.enemies) == 0:
            self.start_next_level()
            return
        new_enemy = self.wave_manager.update(dt, len(self.enemies))
        if new_enemy:
            self.enemies.append(new_enemy)
        for enemy in self.enemies:
            enemy.update(dt)
        self.spatial_hash.clear()
        for enemy in self.enemies:
            self.spatial_hash.insert(enemy)
        for tower in self.towers:
            nearby_enemies = self.spatial_hash.get_nearby(
                tower.pos.x, tower.pos.y, tower.range
            )
            new_projectile = tower.update(dt, nearby_enemies)
            if new_projectile:
                self.projectiles.append(new_projectile)
        for proj in self.projectiles:
            proj.update(dt)
        for enemy in self.enemies:
            if not enemy.is_alive:
                if enemy.reached_base:
                    self.base_hp -= enemy.base_damage
                else:
                    self.money += enemy.reward
        self.enemies = [e for e in self.enemies if e.is_alive]
        self.projectiles = [p for p in self.projectiles if p.is_active]

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map_renderer.render()
        for tower in self.towers:
            target = getattr(tower, "target", None)
            self.game_view.draw_tower(tower, target)
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (int(tower.pos.x), int(tower.pos.y)),
                tower.range,
                1,
            )
        for enemy in self.enemies:
            self.game_view.draw_enemy(enemy)
        for proj in self.projectiles:
            self.game_view.draw_projectile(proj)
        self.hud_view.render(
            self.screen,
            self.base_hp,
            self.money,
            self.wave_manager.current_wave,
        )