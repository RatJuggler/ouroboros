import pygame

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

BLOCK_SIZE = 20
MOVE_DELTA = 20


class Snake:

    def __init__(self):
        self.surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        green = (0, 255, 128)
        self.surface.fill(green)
        self.rectangle = self.surface.get_rect()

    def move(self, pressed):
        if pressed[K_UP]:
            self.rectangle.move_ip(0, -MOVE_DELTA)
        if pressed[K_DOWN]:
            self.rectangle.move_ip(0, MOVE_DELTA)
        if pressed[K_LEFT]:
            self.rectangle.move_ip(-MOVE_DELTA, 0)
        if pressed[K_RIGHT]:
            self.rectangle.move_ip(MOVE_DELTA, 0)
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > DISPLAY_WIDTH:
            self.rectangle.right = DISPLAY_WIDTH
        if self.rectangle.top < 0:
            self.rectangle.top = 0
        if self.rectangle.bottom > DISPLAY_HEIGHT:
            self.rectangle.bottom = DISPLAY_HEIGHT


def play():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Ouroboros')
    clock = pygame.time.Clock()
    snake = Snake()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pressed = pygame.key.get_pressed()
        snake.move(pressed)
        screen.fill((0, 0, 0))
        screen.blit(snake.surface, snake.rectangle)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    play()
    pygame.quit()
