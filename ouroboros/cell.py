import pygame

from typing import Optional

from ouroboros.display import Display
from ouroboros.sprite_images import SpriteImages
from ouroboros.utils import Point

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
FIXED = 'fixed'

OPPOSITE_DIRECTION = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}


class Cell(pygame.sprite.Sprite):

    def __init__(self, display: Display, images: SpriteImages, at_cell: Point, direction: Optional[str]) -> None:
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

    def _move(self, delta: Point) -> bool:
        self._cell = (self._cell[0] + delta[0], self._cell[1] + delta[1])
        self._display.move_ip(self.rect, delta[0], delta[1])
        return self._display.valid_position(self._cell)

    def move_in(self, new_direction: Optional[str]) -> bool:
        if new_direction and new_direction != OPPOSITE_DIRECTION[self._direction]:
            self._direction = new_direction
        if self._direction == UP:
            move = 0, -1
        elif self._direction == DOWN:
            move = 0, 1
        elif self._direction == LEFT:
            move = -1, 0
        elif self._direction == RIGHT:
            move = 1, 0
        else:
            move = 0, 0
        return self._move(move)

    def get_direction(self) -> str:
        return self._direction
