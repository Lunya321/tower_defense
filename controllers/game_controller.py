import pygame
from models.map_model import MapModel
from models.wave_manager import WaveManager
from models.towers import ArrowTower, CannonTower, SlowTower, SniperTower
from views.map_renderer import MapRenderer
from views.hud_view import HudView
from views.tower_panel_view import TowerPanelView
from views.game_view import GameView
from views.menu_view import MenuView
from views.pause_menu_view import PauseMenuView
from views.game_over_view import GameOverView
from views.tower_info_view import TowerInfoView
from algorithms.spatial_hash import SpatialHash

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class GameController:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.state = GameState.MENU
        self.map_model = None
        self.map_renderer = None
        self.hud_view = HudView()
        self.tower_panel = TowerPanelView(self.screen, self.asset_manager)
        self.game_view = GameView(self.screen, self.asset_manager)
        self.menu_view = MenuView(self.screen)
        self.pause_menu = PauseMenuView(self.screen)
        self.game_over_view = GameOverView(self.screen)
        self.tower_info_view = TowerInfoView(self.screen)
        self.wave_manager = None
        self.spatial_hash = SpatialHash(cell_size=120)
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.money = 100
        self.base_hp = 20
        self.enemies_killed = 0
        self.gold_earned = 0
        self.tower_factories = {
            "arrow": ArrowTower,
            "cannon": CannonTower,
            "slow": SlowTower,
            "sniper": SniperTower,
        }

    def start_new_game(self):
        self.map_model = MapModel()
        self.asset_manager.tile_size = self.map_model.tile_size
        self.map_renderer = MapRenderer(self.screen, self.map_model)
        self.wave_manager = WaveManager(
            self.map_model.path, self.map_model.tile_size
        )
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.money = 100
        self.base_hp = 20
        self.enemies_killed = 0
        self.gold_earned = 0
        self.state = GameState.PLAYING

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()

            if self.state == GameState.MENU:
                action = self.menu_view.handle_click(mouse_pos)
                if action == "new_game":
                    self.start_new_game()
                elif action == "quit":
                    pygame.quit()
                    exit()
                return

            if self.state == GameState.PAUSED:
                action = self.pause_menu.handle_click(mouse_pos)
                if action == "resume":
                    self.state = GameState.PLAYING
                elif action == "main_menu":
                    self.state = GameState.MENU
                return

            if self.state == GameState.GAME_OVER:
                action = self.game_over_view.handle_click(mouse_pos)
                if action == "new_game":
                    self.start_new_game()
                elif action == "main_menu":
                    self.state = GameState.MENU
                return

            if self.state == GameState.PLAYING:
                tower_action = self.tower_info_view.handle_click(mouse_pos)
                if tower_action == "upgrade":
                    tower = self.tower_info_view.selected_tower
                    upgrade_cost = int(tower.cost * 0.7)
                    if self.money >= upgrade_cost:
                        self.money -= upgrade_cost
                        tower.damage = int(tower.damage * 1.5)
                        tower.range = int(tower.range * 1.2)
                        tower.cost += upgrade_cost
                    return
                elif tower_action == "sell":
                    tower = self.tower_info_view.selected_tower
                    sell_value = int(tower.cost * 0.5)
                    self.money += sell_value
                    self.towers.remove(tower)
                    self.tower_info_view.close()
                    return

                tower_type = self.tower_panel.handle_click(mouse_pos)
                if tower_type:
                    return

                grid_x = mouse_pos[0] // self.map_model.tile_size
                grid_y = mouse_pos[1] // self.map_model.tile_size

                if self.map_model.get_tile(grid_x, grid_y) == 0:
                    for tower in self.towers:
                        if tower.grid_x == grid_x and tower.grid_y == grid_y:
                            self.tower_info_view.selected_tower = tower
                            return

                    selected_type = self.tower_panel.get_selected_tower()
                    tower_factory = self.tower_factories.get(selected_type)
                    if tower_factory:
                        temp_tower = tower_factory(
                            grid_x, grid_y, self.map_model.tile_size
                        )
                        if self.money >= temp_tower.cost:
                            self.money -= temp_tower.cost
                            self.towers.append(temp_tower)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING

    def update(self, dt):
        if self.state != GameState.PLAYING:
            return

        if self.base_hp <= 0:
            self.state = GameState.GAME_OVER
            return

        if self.wave_manager.current_wave > 5 and len(self.enemies) == 0:
            self.state = GameState.GAME_OVER
            return

        new_enemy = self.wave_manager.update(dt, len(self.enemies))
        if new_enemy:
            self.enemies.append(new_enemy)

        self.spatial_hash.clear()
        for enemy in self.enemies:
            self.spatial_hash.insert(enemy)

        for enemy in self.enemies:
            nearby_enemies = self.spatial_hash.get_nearby(
                enemy.pos.x, enemy.pos.y, 100
            )
            enemy.update(dt, nearby_enemies)

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
                    self.enemies_killed += 1
                    self.gold_earned += enemy.reward

        self.enemies = [e for e in self.enemies if e.is_alive]
        self.projectiles = [p for p in self.projectiles if p.is_active]

    def render(self):
        if self.state == GameState.MENU:
            self.menu_view.render()
            return

        if self.state == GameState.PAUSED:
            self.map_renderer.render()
            for tower in self.towers:
                target = getattr(tower, "target", None)
                self.game_view.draw_tower(tower, target)
            for enemy in self.enemies:
                self.game_view.draw_enemy(enemy)
            self.hud_view.render(
                self.screen,
                self.base_hp,
                self.money,
                self.wave_manager.current_wave,
            )
            self.pause_menu.render()
            return

        if self.state == GameState.GAME_OVER:
            victory = self.wave_manager.current_wave > 5
            self.game_over_view.render(
                victory,
                self.wave_manager.current_wave,
                self.enemies_killed,
                self.gold_earned,
            )
            return

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
        self.tower_panel.render(self.money)
        self.tower_info_view.render(
            self.tower_info_view.selected_tower, self.money
        )