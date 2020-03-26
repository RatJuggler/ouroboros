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
    move_delta = 5
    green = (0, 255, 128)
    surface = pygame.Surface((side, side))
    surface.fill(green)
    rectangle = surface.get_rect()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            rectangle.move_ip(0, -move_delta)
        if pressed[K_DOWN]:
            rectangle.move_ip(0, move_delta)
        if pressed[K_LEFT]:
            rectangle.move_ip(-move_delta, 0)
        if pressed[K_RIGHT]:
            rectangle.move_ip(move_delta, 0)
        screen.fill((0, 0, 0))
        screen.blit(surface, rectangle)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    play()
    pygame.quit()
