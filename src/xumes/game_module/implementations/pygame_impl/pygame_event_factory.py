import pygame

from xumes.game_module.i_game_event import IGameEvent
from xumes.game_module.i_event_factory import IEventFactory
from xumes.game_module.implementations.pygame_impl.pygame_events import Up, Down, Left, Right, Space


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

    def space(self) -> IGameEvent:
        return Space()
