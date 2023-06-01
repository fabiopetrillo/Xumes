import sys
from abc import ABC

import pygame

from framework.game_service_module.game_service import GameService
from framework.game_service_module.game_state_observer import JsonGameStateObserver
from framework.game_service_module.pygame_helpers.pygame_event_factory import PygameEventFactory
from framework.game_service_module.rest_helpers.communication_service_rest_api import CommunicationServiceRestApi
from framework.game_service_module.test_runner import JsonTestRunner
from games_examples.snake.play import Main
from games_examples.snake.test_game_service.snake_observables import SnakeObservable, FruitObservable


class MainTestRunner(Main, JsonTestRunner, ABC):

    def __init__(self, observers):
        Main.__init__(self)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.snake = SnakeObservable(observers, "snake")
        self.fruit = FruitObservable(observers, "fruit")

    def fruit_ate(self):
        super().fruit_ate()
        self.update_state("fruit_ate")

    def game_over(self):
        super().game_over()
        self.update_state("lose")

    def run_test(self) -> None:
        while True:
            self.test_client.wait()
            for event in pygame.event.get():
                self.check_events(event)
            self.update()
            self.clock.tick(0)

    def reset(self) -> None:
        self.snake.detach_all()
        self.fruit.detach_all()

        self.snake = SnakeObservable(self.observers, "snake")
        self.fruit = FruitObservable(self.observers, "fruit")

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) == 2:
        if sys.argv[1] == "-test":
            game_service = GameService(observer=JsonGameStateObserver.get_instance(),
                                       test_runner=MainTestRunner(observers=[JsonGameStateObserver.get_instance()]),
                                       event_factory=PygameEventFactory(),
                                       communication_service=CommunicationServiceRestApi())
            game_service.run()
    else:
        game = Main()
        game.run()
