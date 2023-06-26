import pygame

from games_examples.flappy_bird.params import HEIGHT
from games_examples.flappy_bird.play import Game
from games_examples.flappy_bird.src.pipe import Pipe
from games_examples.flappy_bird.src.pipe_generator import PipeGenerator
from games_examples.flappy_bird.src.player import Player
from xumes.game_module import State
from xumes.game_module.test_manager import given, when, loop, then, render


@given("A game with a player and a pipe generator")
def test_impl(test_context):
    test_context.game = Game()
    test_context.game = test_context.bind(test_context.game, "game",
                                          state=State("terminated", methods_to_observe=["end_game", "reset"]))
    test_context.game.player = test_context.bind(Player(position=HEIGHT // 2, game=test_context.game),
                                                 name="player", state=[
            State("center", methods_to_observe="move"),
            State("speedup", methods_to_observe=["jump", "move"]),
            State("points", methods_to_observe="gain_point")])

    def get_rect(x):
        return [x.left, x.top, x.right, x.bottom]

    test_context.game.pipe_generator = test_context.bind(PipeGenerator(game=test_context.game), name="pipe_generator",
                                                         state=State("pipes",
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


@when("The first pipe is at the bottom and the next pipe is at the top")
def test_impl(test_context):
    test_context.game.pipe_generator.pipes.clear()
    test_context.game.pipe_generator.pipes.append(Pipe())  # Mettre les pipes dans un état particulier
    test_context.game.pipe_generator.pipes.append(Pipe())

    test_context.game.player.reset()


@loop
def test_impl(test_context):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                test_context.game.player.jump()

    # Make all game state modification
    test_context.game.pipe_generator.generator(test_context.game.dt)
    test_context.game.player.move(test_context.game.dt)
    test_context.game.pipe_generator.move(test_context.game.dt)

    test_context.game.dt = 0.09


@then("The player should have passed two pipes")
def test_impl(test_context):
    test_context.assert_equal(test_context.game.player.points, 2)


@render
def test_impl(test_context):
    test_context.game.render()
    pygame.display.flip()

    test_context.game.dt = test_context.game.clock.tick(60) / 1000
