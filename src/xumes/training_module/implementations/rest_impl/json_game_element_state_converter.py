from typing import Tuple

from xumes.training_module.game_element_state import GameElementState
from xumes.training_module.i_game_element_state_converter import IGameElementStateConverter


class JsonGameElementStateConverter(IGameElementStateConverter):

    def convert(self, state_wrapper: Tuple) -> GameElementState:
        name, content = state_wrapper
        element_type = content["__type__"]
        state = {}
        for k in content:
            if k != "__type__":
                state[k] = content[k]

        return GameElementState(name=name, element_type=element_type, state_obj=state)
