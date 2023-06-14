from abc import ABC

from xumes.game_module.game_element_state import GameElementState
from xumes.game_module.state_observable import StateObservable

from games_examples.batkill.src.backend_player import StandardPlayer
from games_examples.batkill.src.spriteful_bat import Bat


class PlayerObservable(StandardPlayer, StateObservable, ABC):

    def __init__(self, ground_y, rect, collider_rect, x_step, attack_cooldown, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        StandardPlayer.__init__(self, ground_y=ground_y, rect=rect, collider_rect=collider_rect, x_step=x_step, attack_cooldown=attack_cooldown)
        self.notify()

    def update(self, actions, dt):
        super().update(actions=actions, dt=dt)
        self.notify()

    def state(self):
        return GameElementState({
            "position": {
                "x": self.x,
                "y": self.y
            },
            "direction": self.facing,
            "jump_stage": self.jump_stage
        })


class BatObservable(Bat, StateObservable, ABC):
    def __init__(self, direction, step, sprite_path, *groups, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Bat.__init__(self, direction, step, sprite_path, *groups)
        self.notify()

    def update(self):
        super().update(self)
        self.notify()

    def state(self):
        return GameElementState({
            "position": {
                "x": self.x,
                "y": self.y
            },
            "direction": self.direction,
            "speed": self.step,
            "dead": self.dead
        })
