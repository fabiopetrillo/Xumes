from xumes.training_module import IStateEntity


class PipesEntity(IStateEntity):

    class Pipe:

        def __init__(self, rect1, rect2):
            self.rect1 = rect1
            self.rect2 = rect2

    def __init__(self, pipes=None):
        if pipes is None:
            pipes = []
        self.pipes = pipes

    def update(self, state) -> None:
        self.pipes.clear()

        for c in state["pipes"]:
            rect1 = [c["rect1"]["left"], c["rect1"]["top"], c["rect1"]["right"], c["rect1"]["bottom"]]
            rect2 = [c["rect2"]["left"], c["rect2"]["top"], c["rect2"]["right"], c["rect2"]["bottom"]]
            self.pipes.append(PipesEntity.Pipe(rect1, rect2))

    @staticmethod
    def build(state):
        pipes = []
        for c in state["pipes"]:
            rect1 = [c["rect1"]["left"], c["rect1"]["top"], c["rect1"]["right"], c["rect1"]["bottom"]]
            rect2 = [c["rect2"]["left"], c["rect2"]["top"], c["rect2"]["right"], c["rect2"]["bottom"]]
            pipes.append(PipesEntity.Pipe(rect1, rect2))

        pipes_entity = PipesEntity(pipes)
        return pipes_entity
