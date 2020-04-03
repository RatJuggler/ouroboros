import pygame

from typing import Dict

from ouroboros.utils import full_file_path


class Sounds:

    def __init__(self, sounds: Dict[str, pygame.mixer.SoundType]) -> None:
        self._sounds = sounds

    @classmethod
    def load_sounds(cls) -> 'Sounds':
        sounds = {'eating': pygame.mixer.Sound(full_file_path('eat.wav')),
                  'died': pygame.mixer.Sound(full_file_path('died.wav'))}
        return Sounds(sounds)

    def play_sound(self, name: str) -> None:
        sound = self._sounds.get(name)
        if sound:
            sound.play()
