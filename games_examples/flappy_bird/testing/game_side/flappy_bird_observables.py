from abc import ABC

from framework.game_service_module.game_element_state import GameElementState
from framework.game_service_module.state_observable import StateObservable
from games_examples.flappy_bird.src.pipe_generator import PipeGenerator
from games_examples.flappy_bird.src.player import Player


class BirdObservable(Player, StateObservable, ABC):

    def __init__(self, position, game, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Player.__init__(self, position, game)
        self.notify()

    def move(self, dt):
        Player.move(self, dt=dt)
        self.notify()

    def state(self):
        return GameElementState({
            "center": {
                "x": self.center()[0],
                "y": self.center()[1]
            },
            "speedup": self.speedup
        })


class PipeGeneratorObservable(PipeGenerator, StateObservable, ABC):

    def __init__(self, game, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        PipeGenerator.__init__(self, game)
        self.notify()

    def generator(self, dt):
        PipeGenerator.generator(self, dt)
        self.notify()

    def move(self, dt):
        PipeGenerator.move(self, dt)
        self.notify()

    def state(self):
        return GameElementState({
            "pipes": [{
                "rect1": {
                    "left": pipe.rect1.left,
                    "top": pipe.rect1.top,
                    "right": pipe.rect1.right,
                    "bottom": pipe.rect1.bottom,
                },
                "rect2": {
                    "left": pipe.rect2.left,
                    "top": pipe.rect2.top,
                    "right": pipe.rect2.right,
                    "bottom": pipe.rect2.bottom,
                },
            } for pipe in self.pipes]
        })

