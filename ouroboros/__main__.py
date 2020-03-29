from typing import Tuple, Optional

import pygame
import random

from pygame.locals import (
    K_UP, K_w,
    K_DOWN, K_s,
    K_LEFT, K_a,
    K_RIGHT, K_d,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

CELL_SIZE = 20
assert DISPLAY_WIDTH % CELL_SIZE == 0, "Display width must be a multiple of the cell size."
assert DISPLAY_HEIGHT % CELL_SIZE == 0, "Display height must be a multiple of the cell size."
CELL_COLUMNS = DISPLAY_WIDTH // CELL_SIZE
CELL_ROWS = DISPLAY_HEIGHT // CELL_SIZE

RGB = Tuple[int, int, int]
BACKGROUND_COLOUR = (64, 64, 64)
GRID_COLOUR = (128, 128, 128)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


class Cell(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface, at_cell_x: int, at_cell_y: int, direction: Optional[str], colour: RGB) -> None:
        super(Cell, self).__init__()
        self._screen = screen
        self._cell_x = at_cell_x
        self._cell_y = at_cell_y
        self._direction = direction
        self._surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self._surface.fill(colour)
        # Must be named 'rect' for use by collision detection API.
        self.rect = self._surface.get_rect(
            topleft=(at_cell_x * CELL_SIZE, at_cell_y * CELL_SIZE)
        )
        self._prev_cell_x = self._cell_x
        self._prev_cell_y = self._cell_y
        self._prev_direction = self._direction

    def render(self) -> None:
        self._screen.blit(self._surface, self.rect)

    def _move(self, delta_x: int, delta_y: int) -> None:
        self._prev_cell_x = self._cell_x
        self._prev_cell_y = self._cell_y
        self._cell_x += delta_x
        self._cell_y += delta_y
        self.rect.move_ip(delta_x * CELL_SIZE, delta_y * CELL_SIZE)

    def _valid_position(self) -> bool:
        return self.rect.left >= 0 and self.rect.right <= DISPLAY_WIDTH and \
            self.rect.top >= CELL_SIZE and self.rect.bottom <= DISPLAY_HEIGHT

    def move_in(self, new_direction: Optional[str]) -> bool:
        self._prev_direction = self._direction
        if new_direction:
            self._direction = new_direction
        if self._direction == UP:
            self._move(0, -1)
        elif self._direction == DOWN:
            self._move(0, 1)
        elif self._direction == LEFT:
            self._move(-1, 0)
        elif self._direction == RIGHT:
            self._move(1, 0)
        return self._valid_position()

    def get_prev_direction(self) -> str:
        return self._prev_direction


class Head(Cell):

    def __init__(self, screen: pygame.Surface, at_x: int, at_y: int) -> None:
        super(Head, self).__init__(screen, at_x, at_y, RIGHT, (64, 128, 64))


class Body(Cell):

    def __init__(self, screen: pygame.Surface, at_cell_x: int, at_cell_y: int, direction: str) -> None:
        super(Body, self).__init__(screen, at_cell_x, at_cell_y, direction, (0, 255, 0))

    @classmethod
    def from_head(cls, head: Head) -> 'Body':
        return Body(head._screen, head._prev_cell_x, head._prev_cell_y, head._prev_direction)


class Tail(Cell):

    def __init__(self, screen: pygame.Surface, at_cell_x: int, at_cell_y: int) -> None:
        super(Tail, self).__init__(screen, at_cell_x, at_cell_y, RIGHT, (96, 128, 96))


class Snake:

    def __init__(self, screen: pygame.Surface, head: Head, tail: Tail) -> None:
        self._screen = screen
        self._head = head
        self._body = []
        self._tail = tail

    @classmethod
    def new_snake(cls, screen: pygame.Surface) -> 'Snake':
        new_snake_x = (CELL_COLUMNS - 1) // 2
        new_snake_y = CELL_ROWS // 2
        head = Head(screen, new_snake_x, new_snake_y)
        tail = Tail(screen, new_snake_x - 1, new_snake_y)
        return Snake(screen, head, tail)

    def move_head(self, new_direction: str) -> bool:
        return self._head.move_in(new_direction) and pygame.sprite.spritecollideany(self._head, self._body) is None

    def grow(self) -> None:
        self._body.insert(0, Body.from_head(self._head))

    def move_body(self) -> None:
        prev_segment = self._head
        for segment in self._body:
            segment.move_in(prev_segment.get_prev_direction())
            prev_segment = segment
        self._tail.move_in(prev_segment.get_prev_direction())

    def render(self) -> None:
        self._head.render()
        for segment in self._body:
            segment.render()
        self._tail.render()

    def found(self, food) -> bool:
        return pygame.sprite.collide_rect(self._head, food)


class Food(Cell):

    def __init__(self, screen: pygame.Surface) -> None:
        super(Food, self).__init__(screen,
                                   random.randint(0, CELL_COLUMNS - 1),
                                   random.randint(1, CELL_ROWS - 1),
                                   None,
                                   (255, 32, 0))


def decode_input(pressed: Tuple[int]) -> Optional[str]:
    new_direction = None
    if pressed[K_UP] or pressed[K_w]:
        new_direction = UP
    if pressed[K_DOWN] or pressed[K_s]:
        new_direction = DOWN
    if pressed[K_LEFT] or pressed[K_a]:
        new_direction = LEFT
    if pressed[K_RIGHT] or pressed[K_d]:
        new_direction = RIGHT
    return new_direction


def draw_background(screen: pygame.Surface) -> None:
    screen.fill(BACKGROUND_COLOUR)
    for grid_row in range(CELL_SIZE, DISPLAY_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (0, grid_row), (DISPLAY_WIDTH, grid_row))
    for grid_column in range(0, DISPLAY_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (grid_column, CELL_SIZE), (grid_column, DISPLAY_HEIGHT))


def display_score(screen: pygame.Surface, score: int) -> None:
    font = pygame.font.SysFont(None, 24)
    score_img = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_img, ((CELL_COLUMNS - 4) * CELL_SIZE, 2))


def play() -> None:
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Ouroboros')
    clock = pygame.time.Clock()
    snake = Snake.new_snake(screen)
    food = Food(screen)
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_SPACE:
                    return
        new_direction = decode_input(pygame.key.get_pressed())
        if not snake.move_head(new_direction):
            return
        if snake.found(food):
            score += 1
            food.kill()
            snake.grow()
            food = Food(screen)
        else:
            snake.move_body()
        draw_background(screen)
        display_score(screen, score)
        snake.render()
        food.render()
        pygame.display.flip()
        clock.tick(15)


if __name__ == '__main__':
    pygame.init()
    play()
    pygame.quit()
