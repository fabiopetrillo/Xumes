import pygame

from game_service_module.game_event import IGameEvent
from game_service_module.event_factory import IEventFactory
from game_service_module.pygame_helpers.pygame_events import Up, Down, Left, Right


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

