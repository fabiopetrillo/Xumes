from abc import ABC

from game_service.game_element_state import GameElementState
from game_service.state_observable import StateObservable
from games_examples.snake.src.fruit import Fruit
from games_examples.snake.src.snake import Snake


class FruitObservable(Fruit, StateObservable, ABC):

    def __init__(self, observers):
        StateObservable.__init__(self, observable_object=self, observers=observers)
        Fruit.__init__(self)
        self.notify()

    def randomize(self):
        super().randomize()
        self.notify()

    def state(self):
        return GameElementState({
            "x": self.x,
            "y": self.y
        })

    def name(self) -> str:
        return "fruit"


class SnakeObservable(Snake, StateObservable, ABC):

    def __init__(self, observers):
        StateObservable.__init__(self, observable_object=self, observers=observers)
        Snake.__init__(self)
        self.notify()

    def move_snake(self):
        super().move_snake()
        self.notify()

    def state(self):
        return GameElementState({
            "body": [{"x": vector.x, "y": vector.y} for vector in self.body],
        })

    def name(self) -> str:
        return "snake"
