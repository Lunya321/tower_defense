import pygame

class GameOverView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_info = pygame.font.SysFont('Arial', 24)
        self.font_button = pygame.font.SysFont('Arial', 20)
        self.buttons = [
            {"text": "Новая игра", "action": "new_game", "rect": pygame.Rect(300, 350, 200, 40)},
            {"text": "Выйти в меню", "action": "main_menu", "rect": pygame.Rect(300, 410, 200, 40)},
        ]

    def render(self, victory=False, wave=1, enemies_killed=0, gold_earned=0):
        self.screen.fill((20, 20, 40))

        if victory:
            title = self.font_title.render("Победа!", True, (0, 255, 0))
        else:
            title = self.font_title.render("Game Over", True, (255, 0, 0))
        title_rect = title.get_rect(center=(400, 150))
        self.screen.blit(title, title_rect)

        info_lines = [
            f"Волна: {wave}",
            f"Убито врагов: {enemies_killed}",
            f"Заработано монет: {gold_earned}",
        ]
        for i, line in enumerate(info_lines):
            text = self.font_info.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 220 + i * 40))
            self.screen.blit(text, text_rect)

        for button in self.buttons:
            mouse_pos = pygame.mouse.get_pos()
            if button["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 100, 150), button["rect"])
            else:
                pygame.draw.rect(self.screen, (60, 60, 80), button["rect"])
            pygame.draw.rect(self.screen, (255, 215, 0), button["rect"], 2)
            
            text = self.font_button.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None