import pygame

class HudView:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.color_text = (255, 255, 255)
        self.color_gold = (255, 215, 0)
        self.color_hp = (255, 50, 50)

    def render(self, surface, hp, money, wave):
        hp_text = self.font.render(f"Base HP: {hp}", True, self.color_hp)
        money_text = self.font.render(f"Gold: {money}", True, self.color_gold)
        wave_text = self.font.render(f"Wave: {wave}", True, self.color_text)

        surface.blit(hp_text, (15, 15))
        surface.blit(money_text, (15, 45))
        surface.blit(wave_text, (680, 15))