import pygame

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_button = pygame.font.SysFont('Arial', 24)
        self.buttons = [
            {"text": "Новая игра", "action": "new_game", "rect": pygame.Rect(300, 250, 200, 50)},
            {"text": "Настройки", "action": "settings", "rect": pygame.Rect(300, 320, 200, 50)},
            {"text": "Выход", "action": "quit", "rect": pygame.Rect(300, 390, 200, 50)},
        ]

    def render(self):
        self.screen.fill((20, 20, 40))
        title = self.font_title.render("Bastion Break", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 150))
        self.screen.blit(title, title_rect)

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