import pygame

class SettingsView:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.font_title = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_label = pygame.font.SysFont('Arial', 20)
        self.font_button = pygame.font.SysFont('Arial', 20)
        self.music_volume = sound_manager.music_volume
        self.sfx_volume = sound_manager.sfx_volume
        self.slider_width = 200
        self.slider_height = 10
        self.buttons = [
            {"text": "Back", "action": "back", "rect": pygame.Rect(300, 450, 200, 40)},
        ]
        self._create_sliders()

    def _create_sliders(self):
        self.music_slider_rect = pygame.Rect(300, 200, self.slider_width, self.slider_height)
        self.sfx_slider_rect = pygame.Rect(300, 280, self.slider_width, self.slider_height)

    def sync_volumes(self):
        self.music_volume = self.sound_manager.music_volume
        self.sfx_volume = self.sound_manager.sfx_volume

    def render(self):
        self.sync_volumes()
        self.screen.fill((20, 20, 40))

        title = self.font_title.render("Settings", True, (255, 215, 0))
        title_rect = title.get_rect(center=(400, 100))
        self.screen.blit(title, title_rect)

        music_label = self.font_label.render("Music Volume", True, (255, 255, 255))
        self.screen.blit(music_label, (300, 160))

        sfx_label = self.font_label.render("SFX Volume", True, (255, 255, 255))
        self.screen.blit(sfx_label, (300, 240))

        pygame.draw.rect(self.screen, (100, 100, 100), self.music_slider_rect)
        music_fill_width = int(self.slider_width * self.music_volume)
        pygame.draw.rect(self.screen, (0, 200, 0), (300, 200, music_fill_width, self.slider_height))

        pygame.draw.rect(self.screen, (100, 100, 100), self.sfx_slider_rect)
        sfx_fill_width = int(self.slider_width * self.sfx_volume)
        pygame.draw.rect(self.screen, (0, 200, 0), (300, 280, sfx_fill_width, self.slider_height))

        music_text = self.font_label.render(f"{int(self.music_volume * 100)}%", True, (255, 255, 255))
        self.screen.blit(music_text, (520, 195))

        sfx_text = self.font_label.render(f"{int(self.sfx_volume * 100)}%", True, (255, 255, 255))
        self.screen.blit(sfx_text, (520, 275))

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

        if self.music_slider_rect.collidepoint(mouse_pos):
            self.music_volume = max(0.0, min(1.0, (mouse_pos[0] - 300) / self.slider_width))
            self.sound_manager.set_music_volume(self.music_volume)
            return None

        if self.sfx_slider_rect.collidepoint(mouse_pos):
            self.sfx_volume = max(0.0, min(1.0, (mouse_pos[0] - 300) / self.slider_width))
            self.sound_manager.set_sfx_volume(self.sfx_volume)
            return None

        return None