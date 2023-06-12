from xumes.training_module import IStateEntity


class BirdEntity(IStateEntity):

    def __init__(self, center, speedup):
        self.center = center
        self.speedup = speedup

    def update(self, state) -> None:
        self.center = state["center"]["x"], state["center"]["y"]
        self.speedup = state["speedup"]

    @staticmethod
    def build(state):
        bird = BirdEntity((state["center"]["x"], state["center"]["y"]), state["speedup"])
        return bird
