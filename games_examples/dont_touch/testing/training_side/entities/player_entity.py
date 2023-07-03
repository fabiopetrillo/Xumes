from xumes.training_module import IStateEntity


class PlayerEntity(IStateEntity):
    def __init__(self, position):
        self.position = position

    def update(self, state):
        self.position = state["position"]["x"], state["position"]["y"]

    @staticmethod
    def build(state):
        player = PlayerEntity((state["position"]["x"], state["position"]["y"]))
        return player
