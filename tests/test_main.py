from unittest import TestCase

from ouroboros.__main__ import play


class TestMain(TestCase):

    def setUp(self) -> None:
        pass

    def test_play(self) -> None:
        play()
