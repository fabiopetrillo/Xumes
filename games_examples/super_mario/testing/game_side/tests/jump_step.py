import pygame

from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game


@given("A game with a player")
def test_impl(test_context):
    def _get_rect(rect):
        return [rect.x, rect.y]

    def _get_attributes(lst):
        return [{
            'type': item.type,
            'position': {
                'x': item.rect.x,
                'y': item.rect.y
            },
            'alive': item.alive,
            'active': item.active,
            'bouncing': item.boucing,
            'onGround': item.onGround
        } for item in lst]

    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["run", "reset"]),
                                            levelname="jump_feature", feature="100-100")
    entities = ["Coin", "CoinBox", "CoinBrick", "EntityBase", "Goomba", "Item", "Koopa", "Mushroom", "RandomBox"]
    test_context.game.mario = test_context.create(Mario, "mario", state=[
            State("rect", func=_get_rect, methods_to_observe="move"),
            State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
            State("ending_level", methods_to_observe="end_level"),
            State("levelObj", State("entityList", [State(entity, func=_get_attributes) for entity in entities]),
                  methods_to_observe=["_onCollisionWithItem", "_onCollisionWithMob"]),
            State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                      "_onCollisionWithBlock",
                                                                                      "killEntity",
                                                                                      "_onCollisionWithItem"])
    ],
                                                  x=0, y=0, level=test_context.game.level,
                                                  screen=test_context.game.screen,
                                                  dashboard=test_context.game.dashboard, sound=test_context.game.sound,
                                                  gravity=0.8)


@when("The first pipe is at {i} % and the next pipe is at {j} %")
def test_impl(test_context, i, j):
    test_context.game.reset(str(i, "-", j))
    test_context.game.clock.tick(0)


@loop
def test_impl(test_context):
    pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(test_context.game.clock.get_fps())))
    test_context.game.level.drawLevel(test_context.game.mario.camera)
    test_context.game.dashboard.update()
    test_context.game.mario.update()
    #test_context.game.render()

    if test_context.game.mario.restart:
        test_context.game.terminated = True
        test_context.game.reset()


@then("The player should have passed {nb_pipes} pipes")
def test_impl(test_context, nb_pipes):
    test_context.greater_equal(test_context.game.mario.rect.x, 448)


@then("The player should have passed at least {nb_pipes} pipes")
def test_impl(test_context, nb_pipes):
    test_context.assert_greater_equal(test_context.game.mario.rect.x, 320)


@render
def test_impl(test_context):
    # Background
    pygame.display.update()
    test_context.game.clock.tick(test_context.game.max_frame_rate)

    test_context.game.dt = test_context.game.clock.tick(60) / 1000


@log
def test_impl(test_context):
    x, y = test_context.game.player.center
    return {
        "player": {
            "points": test_context.game.player.points,
            "x": x,
            "y": y,
        },
    }
