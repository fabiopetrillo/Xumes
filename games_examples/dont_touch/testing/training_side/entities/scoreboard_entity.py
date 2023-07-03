from xumes.training_module import IStateEntity


class ScoreBoardEntity(IStateEntity):
    def __init__(self, current_score,  max_score):
        self.current_score = current_score
        self.max_score = max_score

    def update(self, state):
        self.current_score = state["current_score"]
        self.max_score = state["max_score"]

    @staticmethod
    def build(state):
        scoreboard = ScoreBoardEntity((state["current_score"], state["max_score"]))
        return scoreboard
