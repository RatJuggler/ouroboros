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


def play():
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption('Ouroboros')
    clock = pygame.time.Clock()
    side = 20
    x = (DISPLAY_WIDTH - side) / 2
    y = (DISPLAY_HEIGHT - side) / 2
    green = (0, 255, 128)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]: y -= 3
        if pressed[K_DOWN]: y += 3
        if pressed[K_LEFT]: x -= 3
        if pressed[K_RIGHT]: x += 3
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, green, pygame.Rect(x, y, side, side))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    play()
    pygame.quit()
