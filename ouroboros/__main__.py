from typing import Tuple

import pygame
import random

from pygame.locals import (
    K_UP, K_w,
    K_DOWN, K_s,
    K_LEFT, K_a,
    K_RIGHT, K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

CELL_SIZE = 20
assert DISPLAY_WIDTH % CELL_SIZE == 0, "Display width must be a multiple of the cell size."
assert DISPLAY_HEIGHT % CELL_SIZE == 0, "Display height must be a multiple of the cell size."
CELL_WIDTH = DISPLAY_WIDTH // CELL_SIZE
CELL_HEIGHT = DISPLAY_HEIGHT // CELL_SIZE

BACKGROUND_COLOUR = (64, 64, 64)
GRID_COLOUR = (128, 128, 128)

MOVE_UP = 'up'
MOVE_DOWN = 'down'
MOVE_LEFT = 'left'
MOVE_RIGHT = 'right'


class Cell(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface, at_cell_x: int, at_cell_y: int, colour: Tuple[int, int, int]) -> None:
        super(Cell, self).__init__()
        self._screen = screen
        self._surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self._surface.fill(colour)
        self.rectangle = self._surface.get_rect(
            topleft=(at_cell_x * CELL_SIZE, at_cell_y * CELL_SIZE)
        )

    def render(self) -> None:
        self._screen.blit(self._surface, self.rectangle)


class Segment(Cell):

    def __init__(self, screen: pygame.Surface, at_cell_x: int, at_cell_y: int) -> None:
        super(Segment, self).__init__(screen, at_cell_x, at_cell_y, (0, 255, 128))

    def slide(self, delta_x: int, delta_y: int) -> None:
        self.rectangle.move_ip(delta_x, delta_y)


class Head(Segment):

    def __init__(self, screen: pygame.Surface, at_x: int, at_y: int) -> None:
        super(Head, self).__init__(screen, at_x, at_y)
        self.prev_x = at_x
        self.prev_y = at_y

    def point(self, direction: str) -> None:
        self.prev_x = self.rectangle.x
        self.prev_y = self.rectangle.y
        if direction == MOVE_UP:
            self.slide(0, -CELL_SIZE)
        if direction == MOVE_DOWN:
            self.slide(0, CELL_SIZE)
        if direction == MOVE_LEFT:
            self.slide(-CELL_SIZE, 0)
        if direction == MOVE_RIGHT:
            self.slide(CELL_SIZE, 0)
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > DISPLAY_WIDTH:
            self.rectangle.right = DISPLAY_WIDTH
        if self.rectangle.top < CELL_SIZE:
            self.rectangle.top = CELL_SIZE
        if self.rectangle.bottom > DISPLAY_HEIGHT:
            self.rectangle.bottom = DISPLAY_HEIGHT


class Snake(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface) -> None:
        super(Snake, self).__init__()
        self._screen = screen
        new_snake_x = (CELL_WIDTH - 1) // 2
        new_snake_y = CELL_HEIGHT // 2
        self._head = Head(self._screen, new_snake_x, new_snake_y)
        self._body = pygame.sprite.OrderedUpdates()
        self._body.add(Segment(self._screen, new_snake_x - 2, new_snake_y))
        self._body.add(Segment(self._screen, new_snake_x - 1, new_snake_y))

    def point(self, direction: str) -> None:
        self._head.point(direction)

    def move(self) -> None:
        new_x = self._head.prev_x
        new_y = self._head.prev_y
        for segment in self._body:
            old_x = segment.rectangle.x
            old_y = segment.rectangle.y
            segment.slide(new_x - old_x, new_y - old_y)
            new_x = old_x
            new_y = old_y

    def grow(self) -> None:
        self._body.add(Segment(self._screen, self._head.prev_x, self._head.prev_y))

    def render(self) -> None:
        self._head.render()
        for segment in self._body:
            segment.render()

    def found(self, food) -> bool:
        return self._head.rectangle.topleft == food.rectangle.topleft


class Food(Cell):

    def __init__(self, screen: pygame.Surface) -> None:
        super(Food, self).__init__(screen, random.randint(0, CELL_WIDTH - 1), random.randint(1, CELL_HEIGHT - 1), (255, 32, 0))


def decode_input(direction: str, pressed: Tuple[int]) -> str:
    if pressed[K_UP] or pressed[K_w]:
        direction = MOVE_UP
    if pressed[K_DOWN] or pressed[K_s]:
        direction = MOVE_DOWN
    if pressed[K_LEFT] or pressed[K_a]:
        direction = MOVE_LEFT
    if pressed[K_RIGHT] or pressed[K_d]:
        direction = MOVE_RIGHT
    return direction


def draw_background(screen: pygame.Surface) -> None:
    screen.fill(BACKGROUND_COLOUR)
    for grid_row in range(0, DISPLAY_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (0, grid_row), (DISPLAY_WIDTH, grid_row))
    for grid_column in range(0, DISPLAY_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOUR, (grid_column, 0), (grid_column, DISPLAY_HEIGHT))


def display_score(screen: pygame.Surface, score: int) -> None:
    font = pygame.font.SysFont(None, 24)
    score_img = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_img, ((CELL_WIDTH - 4) * CELL_SIZE, 2))


def play() -> None:
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Ouroboros')
    clock = pygame.time.Clock()
    snake = Snake(screen)
    food = Food(screen)
    direction = MOVE_RIGHT
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        direction = decode_input(direction, pygame.key.get_pressed())
        snake.point(direction)
        if snake.found(food):
            score += 1
            snake.grow()
            food = Food(screen)
        snake.move()
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
