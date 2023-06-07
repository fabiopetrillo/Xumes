from typing import Tuple, TypeVar

from framework.training_service_module.game_element_state import GameElementState

SW = TypeVar("SW")


class IGameElementStateConverter:

    def convert(self, state_wrapper: SW) -> GameElementState:  # TODO add type to state_wrapper
        """
        Converts a state element to a game element state.
        A game element state is easier to work with in order the build entities.
        :param state_wrapper: element of the game state list.
        """
        raise NotImplementedError


class JsonGameElementStateConverter(IGameElementStateConverter):

    def convert(self, state_wrapper: Tuple) -> GameElementState:
        name, content = state_wrapper
        element_type = content["__type__"]
        state = {}
        for k in content:
            if k != "__type__":
                state[k] = content[k]

        return GameElementState(name=name, element_type=element_type, state_obj=state)
