from abc import ABC

from xumes.game_module.game_element_state import GameElementState
from xumes.game_module.state_observable import StateObservable

from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.hand_side import HandSide
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.components.scoreboard import Scoreboard


class PlayerObservable(Player, StateObservable, ABC):

    def __init__(self, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Player.__init__()
        self.notify()

    def update(self):
        super().update()
        self.notify()

    def state(self):
        return GameElementState({
            "position": {
                "x": self.pos[0],
                "y": self.pos[1]
            }
        })


class HandObservable(Hand, StateObservable, ABC):

    def __init__(self, hand_side: HandSide, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Hand.__init__(self, hand_side)
        self.notify()

    def move(self, scoreboard: Scoreboard, player_position):
        super().move(scoreboard=scoreboard, player_position=player_position)
        self.notify()

    def state(self):
        return GameElementState({
            "position": {
                "x": self.new_x,
                "y": self.new_y
            }
        })