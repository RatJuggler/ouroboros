from typing import Dict

import pygame

from ouroboros.display import Display


class SpriteImages:

    def __init__(self, display: Display, images: Dict[str, pygame.Surface]) -> None:
        self._display = display
        self._images = images

    @classmethod
    def load_images(cls, display: Display, for_class: str) -> 'SpriteImages':
        if for_class == 'Head':
            return SpriteImages(display, {'': display.create_surface((64, 128, 64))})
        elif for_class == 'Body':
            return SpriteImages(display, {'': display.create_surface((0, 255, 0))})
        elif for_class == 'Tail':
            return SpriteImages(display, {'': display.create_surface((96, 128, 96))})
        elif for_class == 'Food':
            return SpriteImages(display, {'': display.create_surface((255, 32, 0))})

    def get_image(self, for_class: str) -> pygame.Surface:
        return self._images[for_class]
