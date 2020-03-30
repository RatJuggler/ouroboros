import pygame

from ouroboros.cell import Cell
from ouroboros.direction import RIGHT
from ouroboros.display import Display


class Head(Cell):

    def __init__(self, display: Display, at_x: int, at_y: int) -> None:
        super(Head, self).__init__(display, at_x, at_y, RIGHT, (64, 128, 64))
        self._prev_cell_x = None
        self._prev_cell_y = None
        self._prev_direction = None

    def mark_prev(self) -> None:
        self._prev_cell_x = self._cell_x
        self._prev_cell_y = self._cell_y
        self._prev_direction = self._direction

    def get_prev_direction(self) -> str:
        return self._prev_direction

    def grow_body(self) -> 'Body':
        return Body(self._display, self._prev_cell_x, self._prev_cell_y, self._prev_direction)


class Body(Cell):

    def __init__(self, display: Display, at_cell_x: int, at_cell_y: int, direction: str) -> None:
        super(Body, self).__init__(display, at_cell_x, at_cell_y, direction, (0, 255, 0))


class Tail(Cell):

    def __init__(self, display: Display, at_cell_x: int, at_cell_y: int) -> None:
        super(Tail, self).__init__(display, at_cell_x, at_cell_y, RIGHT, (96, 128, 96))


class Snake:

    def __init__(self, display: Display, head: Head, tail: Tail) -> None:
        self._diplay = display
        self._head = head
        self._body = []
        self._tail = tail

    @classmethod
    def new_snake(cls, display: Display) -> 'Snake':
        new_snake_x = display.get_center_column()
        new_snake_y = display.get_center_row()
        head = Head(display, new_snake_x, new_snake_y)
        tail = Tail(display, new_snake_x - 1, new_snake_y)
        return Snake(display, head, tail)

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
        self._head.render()
        for segment in self._body:
            segment.render()
        self._tail.render()

    def found(self, food) -> bool:
        return pygame.sprite.collide_rect(self._head, food)
