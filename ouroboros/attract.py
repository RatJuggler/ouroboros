import pygame

from ouroboros.display import Display

from pygame.locals import (
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Attract:
    """
    The attract/title screen.
    """

    def __init__(self, display: Display) -> None:
        self._display = display

    def show_attract(self) -> bool:
        """
        Show the screen then wait for key to start the game.
        :return: True to start the game otherwise exit
        """
        self._display.show_attract()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                    if event.key == K_SPACE:
                        return True
