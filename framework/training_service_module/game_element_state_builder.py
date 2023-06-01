from typing import Tuple

from framework.training_service_module.game_element_state import GameElementState


class IGameElementStateBuilder:

    def build(self, state_wrapper) -> GameElementState:  # TODO add type to state_wrapper
        pass


class JsonGameElementStateBuilder(IGameElementStateBuilder):

    def build(self, state_wrapper: Tuple) -> GameElementState:
        name, content = state_wrapper
        element_type = content["__type__"]
        state = {}
        for k in content:
            if k != "__type__":
                state[k] = content[k]

        return GameElementState(name=name, element_type=element_type, state_obj=state)
