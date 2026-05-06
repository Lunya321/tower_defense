import pygame

class HudView:
    def __init__(self):
        pygame.font.init()
        self.font_large = pygame.font.SysFont('Arial', 32, bold=True)
        
        self.color_hp = (255, 50, 50)
        self.color_gold = (255, 215, 0)
        self.color_wave = (255, 255, 255)

    def render(self, screen, base_hp, money, current_wave):
        hp_surface = self.font_large.render(f"Base HP: {base_hp}", True, self.color_hp)
        money_surface = self.font_large.render(f"Gold: {money}", True, self.color_gold)
        wave_surface = self.font_large.render(f"Wave: {current_wave}", True, self.color_wave)

        screen.blit(hp_surface, (20, 20))
        screen.blit(money_surface, (20, 60))
        
        screen_width = screen.get_width()
        wave_rect = wave_surface.get_rect(topright=(screen_width - 20, 20))
        screen.blit(wave_surface, wave_rect)