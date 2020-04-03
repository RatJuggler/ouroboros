import json
import pygame

from typing import Dict

from ouroboros.display import Display
from ouroboros.utils import full_file_path


class SpriteImages:

    def __init__(self, display: Display, images: Dict[str, Dict[str, pygame.Surface]]) -> None:
        self._display = display
        self._images = images

    @classmethod
    def load_images(cls, display: Display) -> 'SpriteImages':
        image_sheet = pygame.image.load(full_file_path('oroborus.png'))
        images = {}
        with open(full_file_path('sprite_images.json')) as json_file:
            sprite_images = json.load(json_file)
            for for_class, direction_images in sprite_images.items():
                class_images = {}
                image_details = sprite_images[for_class]
                for direction, image_start in image_details.items():
                    class_images[direction] = display.create_surface(image_sheet, tuple(map(int, image_start.split(', '))))
                images[for_class] = class_images
        return SpriteImages(display, images)

    def get_image(self, for_class: str, for_direction: str) -> pygame.Surface:
        return self._images[for_class][for_direction]
