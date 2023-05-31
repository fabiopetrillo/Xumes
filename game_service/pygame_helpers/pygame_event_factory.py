import pygame

from game_service.game_event import IGameEvent
from game_service.event_factory import IEventFactory
from game_service.pygame_helpers.pygame_events import Up, Down, Left, Right


class PygameEventFactory(IEventFactory):

    def clear(self):
        pygame.event.clear()

    def up(self) -> IGameEvent:
        return Up()

    def down(self) -> IGameEvent:
        return Down()

    def left(self) -> IGameEvent:
        return Left()

    def right(self) -> IGameEvent:
        return Right()

