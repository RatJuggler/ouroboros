import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

CELL_SIZE = 20
assert DISPLAY_WIDTH % CELL_SIZE == 0, "Display width must be a multiple of the cell size."
assert DISPLAY_HEIGHT % CELL_SIZE == 0, "Display height must be a multiple of the cell size."
CELL_WIDTH = int(DISPLAY_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(DISPLAY_HEIGHT / CELL_SIZE)

BACKGROUND_COLOUR = (64, 64, 64)
GRID_COLOUR = (128, 128, 128)


class Snake:

    def __init__(self):
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.surface.fill((0, 255, 128))
        self.rectangle = self.surface.get_rect(
            topleft=((CELL_WIDTH - 1) // 2 * CELL_SIZE, (CELL_HEIGHT - 1) // 2 * CELL_SIZE)
        )

    def move(self, pressed):
        if pressed[K_UP]:
            self.rectangle.move_ip(0, -CELL_SIZE)
        if pressed[K_DOWN]:
            self.rectangle.move_ip(0, CELL_SIZE)
        if pressed[K_LEFT]:
            self.rectangle.move_ip(-CELL_SIZE, 0)
        if pressed[K_RIGHT]:
            self.rectangle.move_ip(CELL_SIZE, 0)
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > DISPLAY_WIDTH:
            self.rectangle.right = DISPLAY_WIDTH
        if self.rectangle.top < 0:
            self.rectangle.top = 0
        if self.rectangle.bottom > DISPLAY_HEIGHT:
            self.rectangle.bottom = DISPLAY_HEIGHT


class Food:

    def __init__(self):
        self.surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.surface.fill((255, 32, 0))
        self.rectangle = self.surface.get_rect(
            topleft=(random.randint(0, CELL_WIDTH - 1) * CELL_SIZE, random.randint(0, CELL_HEIGHT - 1) * CELL_SIZE)
        )


def play():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Ouroboros')
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pressed = pygame.key.get_pressed()
        snake.move(pressed)
        screen.fill(BACKGROUND_COLOUR)
        for grid_row in range(CELL_HEIGHT):
            pygame.draw.line(screen, GRID_COLOUR, (0, grid_row * CELL_SIZE), (DISPLAY_WIDTH, grid_row * CELL_SIZE))
        for grid_column in range(CELL_WIDTH):
            pygame.draw.line(screen, GRID_COLOUR, (grid_column * CELL_SIZE, 0), (grid_column * CELL_SIZE, DISPLAY_HEIGHT))
        screen.blit(snake.surface, snake.rectangle)
        screen.blit(food.surface, food.rectangle)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    play()
    pygame.quit()
