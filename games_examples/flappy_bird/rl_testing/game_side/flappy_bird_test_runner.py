import sys

import pygame

from framework.game_service_module.game_service import GameService
from framework.game_service_module.i_game_state_observer import JsonGameStateObserver
from framework.game_service_module.implementations.mq_impl.communication_service_game_mq import \
    CommunicationServiceGameMq
from framework.game_service_module.implementations.pygame_impl.pygame_event_factory import PygameEventFactory
from framework.game_service_module.test_runner import JsonTestRunner
from games_examples.flappy_bird.play import Game, BACKGROUND_COLOR
from games_examples.flappy_bird.rl_testing.game_side.flappy_bird_observables import BirdObservable, \
    PipeGeneratorObservable


class FlappyBirdTestRunner(Game, JsonTestRunner):

    def __init__(self, observers):
        Game.__init__(self)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.player = BirdObservable(position=self.height // 2, game=self, name="bird", observers=observers)
        self.pipe_generator = PipeGeneratorObservable(game=self, name="pipes", observers=observers)

    def check_end(self):
        if self.terminated:
            self.update_state("lose")

    def run_test(self) -> None:
        while self.running:
            self.test_client.wait()
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            # Make all game state modification
            self.pipe_generator.generator(self.dt)
            self.player.move(self.dt)
            self.pipe_generator.move(self.dt)

            if self.player.reward:
                self.update_state("reward")

            self.check_end()

            self.dt = 0.09

    def run_test_render(self) -> None:
        while self.running:
            self.test_client.wait()
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

            # Background
            self.screen.fill(BACKGROUND_COLOR)

            # Make all game state modification
            self.pipe_generator.generator(self.dt)
            self.player.move(self.dt)
            self.pipe_generator.move(self.dt)

            if self.player.reward:
                self.update_state("reward")

            self.check_end()

            self.render()
            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000

    def reset(self):
        Game.reset(self)
        self.pipe_generator.notify()
        self.player.notify()

    def random_reset(self) -> None:
        self.pipe_generator.reset_random()
        self.player.reset_random(self.pipe_generator.pipes)
        self.terminated = False
        self.pipe_generator.notify()
        self.player.notify()

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) == 2:
        game_service = GameService(observer=JsonGameStateObserver.get_instance(),
                                   test_runner=FlappyBirdTestRunner(observers=[JsonGameStateObserver.get_instance()]),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()
