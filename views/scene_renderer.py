import pygame

class SceneRenderer:
    def __init__(self, screen, game_view, hud_view, tower_panel_view, tower_info_view):
        self.screen = screen
        self.game_view = game_view
        self.hud_view = hud_view
        self.tower_panel_view = tower_panel_view
        self.tower_info_view = tower_info_view

    def render_playing(self, map_renderer, towers, enemies, projectiles, effects, money, base_hp, current_wave, current_level):
        self.screen.fill((0, 0, 0))
        map_renderer.render()
        for tower in towers:
            target = getattr(tower, "target", None)
            self.game_view.draw_tower(tower, target)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(tower.pos.x), int(tower.pos.y)), tower.range, 1)
        for enemy in enemies:
            self.game_view.draw_enemy(enemy)
        for proj in projectiles:
            self.game_view.draw_projectile(proj)
        for effect in effects:
            self.game_view.draw_effect(effect)
        self.hud_view.render(self.screen, base_hp, money, current_wave, current_level)
        self.tower_panel_view.render(money)
        self.tower_info_view.render(self.tower_info_view.selected_tower, money)

    def render_paused(self, map_renderer, towers, enemies, money, base_hp, current_wave, current_level, pause_menu):
        map_renderer.render()
        for tower in towers:
            target = getattr(tower, "target", None)
            self.game_view.draw_tower(tower, target)
        for enemy in enemies:
            self.game_view.draw_enemy(enemy)
        self.hud_view.render(self.screen, base_hp, money, current_wave, current_level)
        pause_menu.render()

    def render_game_over(self, game_over_view, victory, current_wave, enemies_killed, gold_earned):
        game_over_view.render(victory, current_wave, enemies_killed, gold_earned)

    def render_menu(self, menu_view):
        menu_view.render()

    def render_settings(self, settings_view):
        settings_view.render()

    def render_victory(self, victory_view, level, enemies_killed, towers_count, base_hp, gold_earned):
        victory_view.render(level, enemies_killed, towers_count, base_hp, gold_earned)