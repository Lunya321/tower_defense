import pygame
from controllers.state_manager import GameState
from models.towers import ArrowTower, CannonTower, SlowTower, SniperTower

class InputHandler:
    def __init__(self, state_manager, menu_view, pause_menu, game_over_view, tower_panel_view, tower_info_view, settings_view, victory_view, sound_manager):
        self.state_manager = state_manager
        self.menu_view = menu_view
        self.pause_menu = pause_menu
        self.game_over_view = game_over_view
        self.tower_panel_view = tower_panel_view
        self.tower_info_view = tower_info_view
        self.settings_view = settings_view
        self.victory_view = victory_view
        self.sound_manager = sound_manager
        self.tower_factories = {
            "arrow": ArrowTower,
            "cannon": CannonTower,
            "slow": SlowTower,
            "sniper": SniperTower,
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(pygame.mouse.get_pos())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._handle_escape_key()

    def _is_click_in_ui(self, mouse_pos):
        if self.tower_info_view.selected_tower:
            panel_x = 620
            panel_y = 50
            panel_width = 170
            panel_height = 180
            panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            if panel_rect.collidepoint(mouse_pos):
                return True
        return False

    def _handle_mouse_click(self, mouse_pos):
        state = self.state_manager.state

        if state == GameState.MENU:
            action = self.menu_view.handle_click(mouse_pos)
            if action == "new_game":
                self.state_manager.start_new_game()
                self.sound_manager.play_music("background_music.ogg")
            elif action == "settings":
                self.state_manager.enter_settings()
            elif action == "quit":
                pygame.quit()
                exit()
            return

        if state == GameState.SETTINGS:
            action = self.settings_view.handle_click(mouse_pos)
            if action == "back":
                self.state_manager.exit_settings()
            return

        if state == GameState.PAUSED:
            action = self.pause_menu.handle_click(mouse_pos)
            if action == "resume":
                self.state_manager.state = GameState.PLAYING
            elif action == "settings":
                self.state_manager.enter_settings()
            elif action == "main_menu":
                self.state_manager.state = GameState.MENU
            return

        if state == GameState.GAME_OVER:
            action = self.game_over_view.handle_click(mouse_pos)
            if action == "new_game":
                self.state_manager.start_new_game()
            elif action == "main_menu":
                self.state_manager.state = GameState.MENU
            return

        if state == GameState.VICTORY:
            action = self.victory_view.handle_click(mouse_pos)
            if action == "next_level":
                self.state_manager.next_level()
            elif action == "main_menu":
                self.state_manager.state = GameState.MENU
            return

        if state == GameState.PLAYING:
            if self._is_click_in_ui(mouse_pos):
                tower_action = self.tower_info_view.handle_click(mouse_pos)
                if tower_action == "close":
                    return
                if tower_action == "upgrade":
                    tower = self.tower_info_view.selected_tower
                    upgrade_cost = int(tower.cost * 0.7)
                    if self.state_manager.money >= upgrade_cost:
                        self.state_manager.money -= upgrade_cost
                        tower.damage = int(tower.damage * 1.5)
                        tower.range = int(tower.range * 1.2)
                        tower.cost += upgrade_cost
                    return
                elif tower_action == "sell":
                    tower = self.tower_info_view.selected_tower
                    sell_value = int(tower.cost * 0.5)
                    self.state_manager.money += sell_value
                    self.state_manager.towers.remove(tower)
                    self.tower_info_view.close()
                    return
                return

            tower_type = self.tower_panel_view.handle_click(mouse_pos)
            if tower_type:
                return

            grid_x = mouse_pos[0] // self.state_manager.map_model.tile_size
            grid_y = mouse_pos[1] // self.state_manager.map_model.tile_size

            if self.state_manager.map_model.get_tile(grid_x, grid_y) == 0:
                for tower in self.state_manager.towers:
                    if tower.grid_x == grid_x and tower.grid_y == grid_y:
                        self.tower_info_view.selected_tower = tower
                        return

                selected_type = self.tower_panel_view.get_selected_tower()
                tower_factory = self.tower_factories.get(selected_type)
                if tower_factory:
                    temp_tower = tower_factory(grid_x, grid_y, self.state_manager.map_model.tile_size)
                    if self.state_manager.money >= temp_tower.cost:
                        self.state_manager.money -= temp_tower.cost
                        self.state_manager.towers.append(temp_tower)
                        self.sound_manager.play_sfx("tower_build")

    def _handle_escape_key(self):
        if self.state_manager.state == GameState.PLAYING:
            self.state_manager.state = GameState.PAUSED
        elif self.state_manager.state == GameState.PAUSED:
            self.state_manager.state = GameState.PLAYING
        elif self.state_manager.state == GameState.SETTINGS:
            self.state_manager.exit_settings()