import pygame

from typing import Optional, Tuple

from ouroboros.direction import move_in, OPPOSITE_DIRECTION
from ouroboros.display import Display
from ouroboros.sprite_images import SpriteImages


class Cell(pygame.sprite.Sprite):

    def __init__(self, display: Display, images: SpriteImages, at_cell: Tuple[int, int], direction: Optional[str]) -> None:
        super(Cell, self).__init__()
        self._display = display
        self._images = images
        self._cell = at_cell
        self._direction = direction
        # Must be named 'rect' for use by collision detection API.
        self.rect = display.get_rect(at_cell)

    def render(self, following_direction: str = 'none') -> str:
        image_key = self._direction
        if following_direction != 'none':
            image_key += '-' + following_direction
        image = self._images.get_image(type(self).__name__, image_key)
        self._display.blit(image, self.rect)
        return self._direction

    def _move(self, delta_x: int, delta_y: int) -> bool:
        self._cell = (self._cell[0] + delta_x, self._cell[1] + delta_y)
        self._display.move_ip(self.rect, delta_x, delta_y)
        return self._display.valid_position(self._cell)

    def move_in(self, new_direction: Optional[str]) -> bool:
        if new_direction and new_direction != OPPOSITE_DIRECTION[self._direction]:
            self._direction = new_direction
        movement = move_in(self._direction)
        return self._move(movement[0], movement[1])

    def get_direction(self) -> str:
        return self._direction
