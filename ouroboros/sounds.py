from typing import Dict

import pygame


class Sounds:

    def __init__(self, sounds: Dict[str, pygame.mixer.SoundType]) -> None:
        self._sounds = sounds

    @classmethod
    def load_sounds(cls) -> 'Sounds':
        sounds = {'eating': pygame.mixer.Sound('eat.wav'),
                  'died': pygame.mixer.Sound('died.wav')}
        return Sounds(sounds)

    def play_sound(self, name: str) -> None:
        sound = self._sounds.get(name)
        if sound:
            sound.play()
