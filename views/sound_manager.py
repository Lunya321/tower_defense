import os
import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self._load_sounds()

    def _load_sounds(self):
        sounds_dir = os.path.join("assets", "sounds")
        sfx_files = [
            "arrow_shoot",
            "cannon_shoot",
            "enemy_death",
            "base_hit",
            "tower_build",
            "game_over",
        ]
        for name in sfx_files:
            path = os.path.join(sounds_dir, f"{name}.wav")
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
                self.sounds[name].set_volume(self.sfx_volume)

    def play_sfx(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, name, loops=-1):
        path = os.path.join("assets", "sounds", name)
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)