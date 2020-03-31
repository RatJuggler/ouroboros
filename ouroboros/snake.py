import pygame

from typing import Tuple

from ouroboros.cell import Cell
from ouroboros.direction import RIGHT
from ouroboros.display import Display
from ouroboros.sprite_images import SpriteImages


class Head(Cell):

    def __init__(self, display: Display, images: SpriteImages, at: Tuple[int, int]) -> None:
        super(Head, self).__init__(display, images, at, RIGHT)
        self._prev_cell = None
        self._prev_direction = None

    def mark_prev(self) -> None:
        self._prev_cell = self._cell
        self._prev_direction = self._direction

    def get_prev_direction(self) -> str:
        return self._prev_direction

    def grow_body(self) -> 'Body':
        return Body(self._display, self._images, self._prev_cell, self._prev_direction)


class Body(Cell):

    def __init__(self, display: Display, images: SpriteImages, at_cell: Tuple[int, int], direction: str) -> None:
        super(Body, self).__init__(display, images, at_cell, direction)


class Tail(Cell):

    def __init__(self, display: Display, images: SpriteImages, at_cell: Tuple[int, int]) -> None:
        super(Tail, self).__init__(display, images, at_cell, RIGHT)


class Snake:

    def __init__(self, head: Head, tail: Tail) -> None:
        self._head = head
        self._body = []
        self._tail = tail

    @classmethod
    def new_snake(cls, display: Display, images: SpriteImages) -> 'Snake':
        snake_start = display.get_center()
        head = Head(display, images, snake_start)
        tail = Tail(display, images, (snake_start[0] - 1, snake_start[1]))
        return Snake(head, tail)

    def move_head(self, new_direction: str) -> bool:
        self._head.mark_prev()
        return self._head.move_in(new_direction) and pygame.sprite.spritecollideany(self._head, self._body) is None

    def grow(self) -> None:
        self._body.insert(0, self._head.grow_body())

    def move_body(self) -> None:
        prev_segment_direction = self._head.get_prev_direction()
        for segment in self._body:
            curr_segment_direction = segment.get_direction()
            segment.move_in(prev_segment_direction)
            prev_segment_direction = curr_segment_direction
        self._tail.move_in(prev_segment_direction)

    def render(self) -> None:
        self._head.render(self._head.get_direction())
        for segment in self._body:
            segment.render(segment.get_direction())
        self._tail.render(self._tail.get_direction())

    def found(self, food) -> bool:
        return pygame.sprite.collide_rect(self._head, food)
