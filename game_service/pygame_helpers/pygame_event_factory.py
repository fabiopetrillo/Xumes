import pygame

from game_service.client_event import IClientEvent
from game_service.event_factory import IEventFactory
from game_service.pygame_helpers.pygame_events import Up, Down, Left, Right


class PygameEventFactory(IEventFactory):

    def clear(self):
        pygame.event.clear()

    def up(self) -> IClientEvent:
        return Up()

    def down(self) -> IClientEvent:
        return Down()

    def left(self) -> IClientEvent:
        return Left()

    def right(self) -> IClientEvent:
        return Right()

