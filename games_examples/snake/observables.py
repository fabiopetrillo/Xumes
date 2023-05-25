from abc import ABC

from game_service.state_observable import StateObservable


class FruitObservable(StateObservable, ABC):

    def state(self):
        return {
            "x": self.object.x,
            "y": self.object.y
        }


class SnakeObservable(StateObservable, ABC):

    def state(self):
        return {
            "body": [{"x": vector.x, "y": vector.y} for vector in self.object.body],
        }
