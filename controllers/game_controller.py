import pygame
from controllers.state_manager import StateManager, GameState
from controllers.input_handler import InputHandler
from views.scene_renderer import SceneRenderer
from views.hud_view import HudView
from views.tower_panel_view import TowerPanelView
from views.game_view import GameView
from views.menu_view import MenuView
from views.pause_menu_view import PauseMenuView
from views.game_over_view import GameOverView
from views.tower_info_view import TowerInfoView
from views.settings_view import SettingsView
from views.victory_view import VictoryView
from views.sound_manager import SoundManager
from algorithms.spatial_hash import SpatialHash

class GameController:
    def __init__(self, screen, asset_manager, sound_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.sound_manager = sound_manager
        self.spatial_hash = SpatialHash(cell_size=120)

        self.state_manager = StateManager(screen, asset_manager)

        self.hud_view = HudView()
        self.tower_panel_view = TowerPanelView(screen, asset_manager)
        self.game_view = GameView(screen, asset_manager)
        self.menu_view = MenuView(screen)
        self.pause_menu = PauseMenuView(screen)
        self.game_over_view = GameOverView(screen)
        self.tower_info_view = TowerInfoView(screen)
        self.settings_view = SettingsView(screen, sound_manager)
        self.victory_view = VictoryView(screen)

        self.input_handler = InputHandler(
            self.state_manager, self.menu_view, self.pause_menu,
            self.game_over_view, self.tower_panel_view, self.tower_info_view,
            self.settings_view, self.victory_view, self.sound_manager
        )

        self.scene_renderer = SceneRenderer(
            screen, self.game_view, self.hud_view, self.tower_panel_view, self.tower_info_view
        )

    def handle_input(self, event):
        self.input_handler.handle_event(event)

    def update(self, dt):
        self.state_manager.update(dt, self.spatial_hash, self.sound_manager)

    def render(self):
        state = self.state_manager.state
        sm = self.state_manager
        current_wave = sm.wave_manager.current_wave if sm.wave_manager else 1
        current_level = sm.current_level

        if state == GameState.MENU:
            self.scene_renderer.render_menu(self.menu_view)
        elif state == GameState.SETTINGS:
            self.scene_renderer.render_settings(self.settings_view)
        elif state == GameState.PAUSED:
            self.scene_renderer.render_paused(
                sm.map_renderer, sm.towers, sm.enemies, sm.money, sm.base_hp, current_wave, current_level, self.pause_menu
            )
        elif state == GameState.GAME_OVER:
            self.scene_renderer.render_game_over(
                self.game_over_view, sm.wave_manager.current_wave > 5 if sm.wave_manager else False, current_wave, sm.enemies_killed, sm.gold_earned
            )
        elif state == GameState.VICTORY:
            self.scene_renderer.render_victory(
                self.victory_view, current_level, sm.enemies_killed, len(sm.towers), sm.base_hp, sm.gold_earned
            )
        elif state == GameState.PLAYING:
            self.scene_renderer.render_playing(
                sm.map_renderer, sm.towers, sm.enemies, sm.projectiles, sm.effects,
                sm.money, sm.base_hp, current_wave, current_level
            )