from framework.training_service_module.state_entity import IStateEntity


class SnakeEntity(IStateEntity):

    def __init__(self):
        self.body = []

    def update(self, state) -> None:
        self.body.clear()
        for c in state["body"]:
            vec = [c["x"], c["y"]]
            self.body.append(vec)

    @staticmethod
    def build(state):
        body = []
        for c in state["body"]:
            vec = [c["x"], c["y"]]
            body.append(vec)

        snake = SnakeEntity()
        snake.body = body
        return snake
