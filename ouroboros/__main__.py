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


class Segment(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface, offset: int) -> None:
        super(Segment, self).__init__()
        self.screen = screen
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.surface.fill((0, 255, 128))
        self.rectangle = self.surface.get_rect(
            topleft=((CELL_WIDTH - offset) // 2 * CELL_SIZE, (CELL_HEIGHT - 1) // 2 * CELL_SIZE)
        )

    def slide(self, delta_x: int, delta_y: int) -> None:
        self.rectangle.move_ip(delta_x, delta_y)

    def render(self) -> None:
        self.screen.blit(self.surface, self.rectangle)


class Head(Segment):

    def __init__(self, screen: pygame.Surface, offset: int) -> None:
        super(Head, self).__init__(screen, offset)

    def move(self, direction: str) -> None:
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
        self.screen = screen
        self.segments = pygame.sprite.OrderedUpdates()
        self.head = Head(self.screen, 1)
        self.segments.add(self.head)
        self.segments.add(Segment(self.screen, 2))
        self.segments.add(Segment(self.screen, 3))

    def move(self, direction: str) -> None:
        new_x = self.head.rectangle.x
        new_y = self.head.rectangle.y
        self.head.move(direction)
        for segment in self.segments:
            if segment != self.head:
                old_x = segment.rectangle.x
                old_y = segment.rectangle.y
                segment.slide(new_x - old_x, new_y - old_y)
                new_x = old_x
                new_y = old_y

    def render(self) -> None:
        for segment in self.segments:
            segment.render()

    def found(self, food) -> bool:
        return self.head.rectangle.topleft == food.rectangle.topleft


class Food(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface) -> None:
        super(Food, self).__init__()
        self.screen = screen
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.surface.fill((255, 32, 0))
        self.rectangle = self.surface.get_rect(
            topleft=(random.randint(0, CELL_WIDTH - 1) * CELL_SIZE, random.randint(1, CELL_HEIGHT - 1) * CELL_SIZE)
        )

    def render(self) -> None:
        self.screen.blit(self.surface, self.rectangle)


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
        snake.move(direction)
        if snake.found(food):
            score += 1
            food = Food(screen)
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
