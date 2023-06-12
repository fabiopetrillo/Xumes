from abc import abstractmethod
from typing import Dict, final

from xumes.training_module.i_state_entity import IStateEntity
from xumes.training_module.game_element_state import GameElementState
from xumes.training_module.i_game_element_state_converter import IGameElementStateConverter


class EntityManager(IStateEntity):
    """
       The `EntityManager` class is responsible for managing game entities and updating the game state.

       Attributes:
           _game_element_state_converter: An object implementing the `IGameElementStateConverter` interface for converting game elements to states.
           _entities: A dictionary mapping entity names to their corresponding `IStateEntity` instances.
           _game_state: The current game state.

       Methods:
           update(state): Updates the game state when received.
           game_state: Property representing the current game state.
           get_all(): Retrieves all game observable entities.
           get(name): Retrieves an entity by its name.
           _update(game_element_state): Updates an existing game entity with the provided `game_element_state`.
           _add(game_element_state): Adds a new game entity with the provided `game_element_state`.
           convert(state_wrapper): Converts a game element, updates or adds it to the state.
           build_entity(game_element_state): Builds a game entity based on the provided `game_element_state`.
    """
    def __init__(self,
                 game_element_state_converter: IGameElementStateConverter
                 ):
        self._game_element_state_converter = game_element_state_converter
        self._entities: Dict[str, IStateEntity] = {
            "test_runner": self
        }
        self._game_state: str = ""

    def update(self, state) -> None:
        """
        Update the game state when receive it.
        :param state: game state (ex: "alive", "dead").
        """
        self._game_state = state["state"]

    @property
    @final
    def game_state(self):
        return self._game_state

    @final
    def get_all(self):
        """
        Get every game observables entities.
        :return: every entity
        """
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
        """
        Convert the game element, and update or add it in the state.
        :param state_wrapper: game element from the list receive.
        """
        ges = self._game_element_state_converter.convert(state_wrapper)
        if ges.name in self._entities:
            self._update(ges)
        else:
            self._add(ges)

    @abstractmethod
    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        """
        Implements a way to redirect the building of game entities.
        Need to call build method from the implemented game entities.
        :param game_element_state:
        """
        raise NotImplementedError
