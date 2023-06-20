import sys

import pygame

from games_examples.flappy_bird.params import HEIGHT
from games_examples.flappy_bird.play import Game, BACKGROUND_COLOR
from games_examples.flappy_bird.src.pipe_generator import PipeGenerator
from games_examples.flappy_bird.src.player import Player
from xumes.game_module import JsonTestRunner, GameService, JsonGameStateObserver, PygameEventFactory, \
    CommunicationServiceGameMq
from xumes.game_module.state_observable import State


class FlappyBirdTestRunner(JsonTestRunner):

    def __init__(self, observers):
        self.game = Game()
        JsonTestRunner.__init__(self, game_loop_object=self.game, observers=observers)
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["end_game", "reset"]))
        self.game.player = self.bind(Player(position=HEIGHT // 2, game=self.game),
                                     name="player", state=[
                State("center", methods_to_observe="move"),
                State("speedup", methods_to_observe=["jump", "move"]),
                State("points", methods_to_observe="gain_point")])

        def get_rect(x):
            return [x.left, x.top, x.right, x.bottom]

        self.game.pipe_generator = self.bind(PipeGenerator(game=self.game), name="pipe_generator", state=State("pipes",
                                                                                                          [
                                                                                                              State(
                                                                                                                  "rect1",
                                                                                                                  func=get_rect),
                                                                                                              State(
                                                                                                                  "rect2",
                                                                                                                  func=get_rect),
                                                                                                          ],
                                                                                                          methods_to_observe="move"
                                                                                                          ))

    def run_test(self) -> None:
        while self.game.running:
            self.test_client.wait()
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.player.jump()

            # Make all game state modification
            self.game.pipe_generator.generator(self.game.dt)
            self.game.player.move(self.game.dt)
            self.game.pipe_generator.move(self.game.dt)

            self.game.dt = 0.09

    def run_test_render(self) -> None:
        while self.game.running:
            self.test_client.wait()
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game.player.jump()

            # Background
            self.game.screen.fill(BACKGROUND_COLOR)

            # Make all game state modification
            self.game.pipe_generator.generator(self.game.dt)
            self.game.player.move(self.game.dt)
            self.game.pipe_generator.move(self.game.dt)

            self.game.render()
            pygame.display.flip()

            self.game.dt = self.game.clock.tick(60) / 1000

    def reset(self):
        self.game.reset()

    def random_reset(self) -> None:
        self.game.pipe_generator.reset_random()
        self.game.player.reset_random(self.game.pipe_generator.pipes)
        self.game.terminated = False

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
