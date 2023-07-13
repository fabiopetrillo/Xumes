import logging
import sys

import pygame

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game

from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State

class SuperMarioTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["run", "reset"]))

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

        def get_dash(item):
            return [item.coins, item.points]

        entities = ["Coin", "CoinBox", "CoinBrick", "EntityBase", "Goomba", "Item", "Koopa", "Mushroom", "RandomBox"]
        self.game.mario = self.bind(Mario(0, 0, self.game.level, self.game.screen, self.game.dashboard, self.game.sound), "mario", state=[
            State("rect", func=_get_rect, methods_to_observe="move"),
            State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
            State("ending_level", methods_to_observe="end_level"),
            State("levelObj", State("entityList", [State(entity, func=_get_attributes) for entity in entities]),
                  methods_to_observe=["_onCollisionWithItem", "_onCollisionWithMob"]),
            State("dashboard", func=get_dash, methods_to_observe=["_onCollisionWithItem", "_onCollisionWithBlock", "killEntity", "_onCollisionWithItem"])
            #State("dashboard", State("coins"), methods_to_observe=["_onCollisionWithItem", "_onCollisionWithBlock"]),
            #State("dashboard", State("points"), methods_to_observe=["killEntity", "_onCollisionWithItem"])
        ])

    def run_test(self) -> None:

        while True:

            self.test_client.wait()
            #pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(self.game.clock.get_fps())))
            #if self.game.mario.pause:
            #    self.game.mario.pauseObj.update()
            #else:
            self.game.level.drawLevel(self.game.mario.camera)
            self.game.dashboard.update()
            self.game.mario.update()
            #self.game.render()

            if self.game.mario.restart:
                self.game.terminated = True
        #    self.game.reset()

    def run_test_render(self) -> None:

        while True:

            self.test_client.wait()
            pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(self.game.clock.get_fps())))
            if self.game.mario.pause:
                self.game.mario.pauseObj.update()
            else:
                self.game.level.drawLevel(self.game.mario.camera)
                self.game.dashboard.update()
                self.game.mario.update()
                self.game.render()

            if self.game.mario.restart or self.game.mario.level_ending:
                self.game.terminated = True
                #self.game.reset()

            #self.game.render()

    def reset(self) -> None:
        self.game.reset()

    def random_reset(self) -> None:
        self.reset()

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-test":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        if sys.argv[1] == "-render":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        game_service = GameService(test_runner=SuperMarioTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()






