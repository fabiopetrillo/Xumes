import pygame

from games_examples.flappy_bird.params import HEIGHT, LEFT_POSITION, SPACE_BETWEEN_PIPES, PIPE_SPACE, PIPE_WIDTH, SIZE
from games_examples.flappy_bird.play import Game, BACKGROUND_COLOR
from games_examples.flappy_bird.src.pipe import Pipe
from games_examples.flappy_bird.src.pipe_generator import PipeGenerator
from games_examples.flappy_bird.src.player import Player
from xumes.game_module import State
from xumes.game_module.test_manager import given, when, loop, then, render, clock_reset


@given("A game with a player and a pipe generator")
def test_impl(test_context):
    test_context.game = Game()
    test_context.game = test_context.bind(test_context.game, "game",
                                          state=State("terminated", methods_to_observe=["end_game", "reset"]))
    test_context.game.player = test_context.bind(Player(position=HEIGHT // 2, game=test_context.game),
                                                 name="player", state=[
            State("center", methods_to_observe=["move", "reset"]),
            State("speedup", methods_to_observe=["jump", "move", "reset"]),
            State("points", methods_to_observe=["gain_point", "reset"])])

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
                                                                     methods_to_observe=["move", "reset"]
                                                                     ))

    test_context.game.dt = 0.09


@when("The first pipe is at the bottom and the next pipe is at the top")
def test_impl(test_context):
    test_context.game.reset_trainer()
    test_context.game.pipe_generator.pipes = [Pipe(player=test_context.game.player,
                                                   generator=test_context.game.pipe_generator,
                                                   height=(HEIGHT - PIPE_SPACE) / 2,
                                                   position=LEFT_POSITION + SIZE / 2 + SPACE_BETWEEN_PIPES - PIPE_WIDTH / 2),
                                              Pipe(player=test_context.game.player,
                                                   generator=test_context.game.pipe_generator,
                                                   height=HEIGHT - 50 - PIPE_SPACE,
                                                   position=LEFT_POSITION + SIZE / 2 + 2 * SPACE_BETWEEN_PIPES - PIPE_WIDTH / 2)]
    test_context.game.pipe_generator.notify()


@loop
def test_impl(test_context):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                test_context.game.player.jump()

    # Make all game state modification
    test_context.game.player.move(test_context.game.dt)
    test_context.game.pipe_generator.move(test_context.game.dt)


@then("The player should have passed two pipes")
def test_impl(test_context):
    test_context.assert_equal(test_context.game.player.points, 2)


@render
def test_impl(test_context):
    # Background
    test_context.game.screen.fill(BACKGROUND_COLOR)

    test_context.game.render()
    pygame.display.flip()

    test_context.game.dt = test_context.game.clock.tick(60) / 1000


@clock_reset
def test_impl(test_context):
    test_context.game.clock.tick(60)
