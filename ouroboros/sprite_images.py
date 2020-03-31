from typing import Dict

import json
import pygame

from ouroboros.display import Display


class SpriteImages:

    def __init__(self, display: Display, images: Dict[str, Dict[str, pygame.Surface]]) -> None:
        self._display = display
        self._images = images

    @classmethod
    def load_images(cls, display: Display) -> 'SpriteImages':
        images = {}
        with open('sprite_images.json') as json_file:
            sprite_images = json.load(json_file)
            for for_class, direction_images in sprite_images.items():
                class_images = {}
                image_details = sprite_images[for_class]
                for direction, colour in image_details.items():
                    class_images[direction] = display.create_surface(tuple(map(int, colour[1:-1].split(', '))))
                images[for_class] = class_images
        return SpriteImages(display, images)

    def get_image(self, for_class: str, for_direction: str) -> pygame.Surface:
        return self._images[for_class][for_direction]
