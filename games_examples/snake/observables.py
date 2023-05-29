from abc import ABC

from game_service.game_element_state import GameElementState
from game_service.state_observable import StateObservable


class FruitObservable(StateObservable, ABC):

    def state(self):
        return GameElementState({
            "x": self.object.x,
            "y": self.object.y
        })


class SnakeObservable(StateObservable, ABC):

    def state(self):
        return GameElementState({
            "body": [{"x": vector.x, "y": vector.y} for vector in self.object.body],
        })


