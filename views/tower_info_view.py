import pygame

class TowerInfoView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_info = pygame.font.SysFont('Arial', 16)
        self.font_button = pygame.font.SysFont('Arial', 14)
        self.selected_tower = None
        self.buttons = [
            {"text": "Улучшить", "action": "upgrade", "rect": pygame.Rect(0, 0, 100, 30)},
            {"text": "Продать", "action": "sell", "rect": pygame.Rect(0, 0, 100, 30)},
            {"text": "Закрыть", "action": "close", "rect": pygame.Rect(0, 0, 100, 30)},
        ]

    def render(self, tower, money):
        if not tower:
            return

        self.selected_tower = tower
        panel_x = 620
        panel_y = 50
        panel_width = 170
        panel_height = 180

        pygame.draw.rect(self.screen, (40, 40, 60), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (255, 215, 0), (panel_x, panel_y, panel_width, panel_height), 2)

        title = self.font_title.render(tower.type_name.capitalize(), True, (255, 215, 0))
        self.screen.blit(title, (panel_x + 10, panel_y + 10))

        info_lines = [
            f"Урон: {tower.damage}",
            f"Дальность: {tower.range}",
            f"Скорость: {tower.cooldown:.1f}с",
        ]
        for i, line in enumerate(info_lines):
            text = self.font_info.render(line, True, (255, 255, 255))
            self.screen.blit(text, (panel_x + 10, panel_y + 40 + i * 25))

        upgrade_cost = int(tower.cost * 0.7)
        sell_value = int(tower.cost * 0.5)

        self.buttons[0]["rect"] = pygame.Rect(panel_x + 10, panel_y + 120, 150, 25)
        self.buttons[1]["rect"] = pygame.Rect(panel_x + 10, panel_y + 150, 150, 25)

        can_upgrade = money >= upgrade_cost
        for i, button in enumerate(self.buttons[:2]):
            mouse_pos = pygame.mouse.get_pos()
            if button["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 100, 150), button["rect"])
            else:
                pygame.draw.rect(self.screen, (60, 60, 80), button["rect"])
            
            text_color = (255, 215, 0) if can_upgrade or i == 1 else (150, 150, 150)
            button_text = f"{button['text']} ({upgrade_cost}g)" if i == 0 else f"Продать ({sell_value}g)"
            text = self.font_button.render(button_text, True, text_color)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, mouse_pos):
        if not self.selected_tower:
            return None

        for button in self.buttons[:2]:
            if button["rect"].collidepoint(mouse_pos):
                return button["action"]
        return None

    def close(self):
        self.selected_tower = None