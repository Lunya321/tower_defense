import os
import pygame

class HudView:
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.SysFont('Arial', 28, bold=True)
        self.font_wave = pygame.font.SysFont('Arial', 22, bold=True)
        self.coin_icon = None
        self._load_coin_icon()

    def _load_coin_icon(self):
        coin_path = os.path.join("assets", "images", "hud", "coin.png")
        if os.path.exists(coin_path):
            img = pygame.image.load(coin_path).convert_alpha()
            self.coin_icon = pygame.transform.scale(img, (28, 28))

    def render(self, screen, base_hp, money, current_wave):
        self._render_hp_bar(screen, base_hp)
        self._render_money(screen, money)
        self._render_wave(screen, current_wave)

    def _render_hp_bar(self, screen, base_hp):
        max_hp = 20
        bar_x = 20
        bar_y = 20
        bar_width = 180
        bar_height = 22

        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height), border_radius=6)

        hp_ratio = max(0, base_hp / max_hp)
        fill_width = int((bar_width - 4) * hp_ratio)
        if fill_width > 0:
            pygame.draw.rect(screen, (220, 40, 40), (bar_x + 2, bar_y + 2, fill_width, bar_height - 4), border_radius=4)

        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=6)

        hp_text = self.font_wave.render(f"{base_hp}/{max_hp}", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(hp_text, hp_rect)

    def _render_money(self, screen, money):
        coin_x = 20
        coin_y = 52

        if self.coin_icon:
            screen.blit(self.coin_icon, (coin_x, coin_y))
            text_x = coin_x + 36
        else:
            pygame.draw.circle(screen, (255, 215, 0), (coin_x + 14, coin_y + 14), 12)
            pygame.draw.circle(screen, (200, 170, 0), (coin_x + 14, coin_y + 14), 12, 2)
            text_x = coin_x + 32

        money_surface = self.font_large.render(f"{money}", True, (255, 215, 0))
        screen.blit(money_surface, (text_x, coin_y))

    def _render_wave(self, screen, current_wave):
        screen_width = screen.get_width()

        bg_rect = pygame.Rect(screen_width - 140, 14, 126, 34)
        pygame.draw.rect(screen, (40, 40, 60), bg_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 215, 0), bg_rect, 2, border_radius=8)

        wave_text = self.font_wave.render(f"WAVE {current_wave}/5", True, (255, 255, 255))
        wave_rect = wave_text.get_rect(center=bg_rect.center)
        screen.blit(wave_text, wave_rect)