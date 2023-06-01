from abc import abstractmethod
from typing import Dict, final

from framework.training_service_module.game_element_state import GameElementState
from framework.training_service_module.game_element_state_builder import IGameElementStateBuilder
from framework.training_service_module.state_entity import IStateEntity


class EntityManager:

    def __init__(self,
                 game_element_state_builder: IGameElementStateBuilder
                 ):
        self._game_element_state_builder = game_element_state_builder
        self._entities: Dict[str, IStateEntity] = {}

    @final
    def get_all(self):
        return self._entities

    @final
    def get(self, name: str):
        return self._entities[name]

    @final
    def _update(self, game_element_state: GameElementState):
        self.get(game_element_state.name).update(game_element_state.state)

    @final
    def _add(self, game_element_state: GameElementState):
        self._entities[game_element_state.name] = self.build_entity(game_element_state)

    @final
    def convert(self, state_wrapper):
        ges = self._game_element_state_builder.build(state_wrapper)
        if ges.name in self._entities:
            self._update(ges)
        else:
            self._add(ges)

    @abstractmethod
    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        pass
