import pygame

from typing import Optional

from ouroboros.direction import move_in
from ouroboros.display import Display, RGB


class Cell(pygame.sprite.Sprite):

    def __init__(self, display: Display, at_cell_x: int, at_cell_y: int, direction: Optional[str], colour: RGB) -> None:
        super(Cell, self).__init__()
        self._display = display
        self._cell_x = at_cell_x
        self._cell_y = at_cell_y
        self._direction = direction
        self._surface = display.get_surface()
        self._surface.fill(colour)
        # Must be named 'rect' for use by collision detection API.
        self.rect = display.get_rect(self._surface, at_cell_x, at_cell_y)

    def render(self) -> None:
        self._display.blit(self._surface, self.rect)

    def _move(self, delta_x: int, delta_y: int) -> bool:
        self._cell_x += delta_x
        self._cell_y += delta_y
        self._display.move_ip(self.rect, delta_x, delta_y)
        return self._display.valid_position(self._cell_x, self._cell_y)

    def move_in(self, new_direction: Optional[str]) -> bool:
        if new_direction:
            self._direction = new_direction
        movement = move_in(self._direction)
        return self._move(movement[0], movement[1])

    def get_direction(self) -> str:
        return self._direction
