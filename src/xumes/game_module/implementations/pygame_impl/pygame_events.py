import pygame

from xumes.game_module.i_game_event import IGameEvent


def key_down(key: pygame.constants):
    # Create and post event "keydown"
    event = pygame.event.Event(pygame.KEYDOWN, key=key)
    pygame.event.post(event)


def key_up(key: pygame.constants):
    # Create and post event "keyup"
    event = pygame.event.Event(pygame.KEYUP, key=key)
    pygame.event.post(event)


class Up(IGameEvent):

    def press(self) -> None:
        key_down(key=pygame.K_UP)

    def release(self) -> None:
        key_up(key=pygame.K_DOWN)


class Down(IGameEvent):

    def press(self) -> None:
        key_down(pygame.K_DOWN)

    def release(self) -> None:
        key_up(pygame.K_DOWN)


class Left(IGameEvent):

    def press(self) -> None:
        key_down(pygame.K_LEFT)

    def release(self) -> None:
        key_up(pygame.K_LEFT)


class Right(IGameEvent):

    def press(self) -> None:
        key_down(pygame.K_RIGHT)

    def release(self) -> None:
        key_up(pygame.K_RIGHT)


class Space(IGameEvent):

    def press(self) -> None:
        key_down(pygame.K_SPACE)

    def release(self) -> None:
        key_up(pygame.K_SPACE)
