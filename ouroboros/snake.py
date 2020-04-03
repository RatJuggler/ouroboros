import pygame

from typing import List, Optional

from ouroboros.cell import Cell, RIGHT
from ouroboros.display import Display
from ouroboros.sounds import Sounds
from ouroboros.sprite_images import SpriteImages
from ouroboros.utils import Point


class Head(Cell):

    def __init__(self, display: Display, images: SpriteImages, at: Point) -> None:
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

    def __init__(self, display: Display, images: SpriteImages, at_cell: Point, direction: str) -> None:
        super(Body, self).__init__(display, images, at_cell, direction)


class Tail(Cell):

    def __init__(self, display: Display, images: SpriteImages, at_cell: Point) -> None:
        super(Tail, self).__init__(display, images, at_cell, RIGHT)


class Snake:

    def __init__(self, head: Head, tail: Tail, sounds: Sounds) -> None:
        self._head = head
        self._body = []
        self._tail = tail
        self._sounds = sounds
        self._eating = False

    @classmethod
    def new_snake(cls, display: Display, images: SpriteImages, sounds: Sounds) -> 'Snake':
        snake_start = display.get_center()
        head = Head(display, images, snake_start)
        tail = Tail(display, images, (snake_start[0] - 1, snake_start[1]))
        return Snake(head, tail, sounds)

    def move_head(self, new_direction: str) -> bool:
        self._head.mark_prev()
        move_ok = self._head.move_in(new_direction) and pygame.sprite.spritecollideany(self._head, self._body) is None
        if not move_ok:
            self._sounds.play_sound('died')
        return move_ok

    def move_body(self) -> None:
        prev_segment_direction = self._head.get_prev_direction()
        for segment in self._body:
            curr_segment_direction = segment.get_direction()
            segment.move_in(prev_segment_direction)
            prev_segment_direction = curr_segment_direction
        self._tail.move_in(prev_segment_direction)

    def render(self) -> None:
        follow_direction = self._head.render(str(self._eating))
        for segment in self._body:
            follow_direction = segment.render(follow_direction)
        self._tail.render(follow_direction)

    def eats(self, cells: List[Cell]) -> Optional[Cell]:
        eats = pygame.sprite.spritecollideany(self._head, cells)
        if eats:
            self._eating = True
            self._body.insert(0, self._head.grow_body())
        else:
            self._eating = False
        return eats

    def is_on(self, cell: Cell) -> bool:
        return pygame.sprite.collide_rect(cell, self._head) or pygame.sprite.spritecollideany(cell, self._body)
