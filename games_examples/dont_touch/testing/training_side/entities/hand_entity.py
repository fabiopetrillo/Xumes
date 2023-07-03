from xumes.training_module import IStateEntity

from games_examples.dont_touch.src.components import hand_side


class HandEntity(IStateEntity):
    def __init__(self, position, side, speed):
        self.side = side
        self.position = position
        self.speed = speed

    def update(self, state):
        self.position = state["position"]["x"], state["position"]["y"]
        self.speed = state["speed"]
        self.side= state["side"]

    @staticmethod
    def build(state):
        hand = HandEntity((state["position"]["x"], state["position"]["y"]), state["speed"], state["side"])
        return hand
