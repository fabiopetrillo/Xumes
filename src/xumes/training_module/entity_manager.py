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


def choose_delegate(value):
    if isinstance(value, bool):
        return DelegateBool(value)
    elif isinstance(value, int):
        return DelegateInt(value)
    elif isinstance(value, float):
        return DelegateFloat(value)
    elif isinstance(value, complex):
        return DelegateComplex(value)
    elif isinstance(value, str):
        return DelegateStr(value)
    elif isinstance(value, list):
        return DelegateList(value)
    elif isinstance(value, tuple):
        return DelegateTuple(value)
    elif isinstance(value, set):
        return DelegateSet(value)
    elif isinstance(value, dict):
        if "__type__" in value:
            return Object(value)
        return DelegateDict(value)


class Delegate:

    def update(self, state):
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError


class DelegateBool(Delegate, int):
    def __init__(self, value):
        bool.__init__(value)

    def update(self, state):
        return DelegateBool(state)

    def __hash__(self):
        return hash(bool(self))


class DelegateInt(Delegate, int):

    def __init__(self, value):
        int.__init__(value)

    def update(self, state):
        return DelegateInt(state)

    def __hash__(self):
        return hash(int(self))


class DelegateFloat(Delegate, float):
    def __init__(self, value):
        float.__init__(value)

    def update(self, state):
        return DelegateFloat(state)

    def __hash__(self):
        return hash(float(self))


class DelegateComplex(Delegate, complex):
    def __init__(self, value):
        complex.__init__(value)

    def update(self, state):
        return DelegateComplex(state)

    def __hash__(self):
        return hash(complex(self))


class DelegateStr(Delegate, str):
    def __init__(self, value):
        str.__init__(value)

    def update(self, state):
        return DelegateStr(state)

    def __hash__(self):
        return hash(str(self))


class DelegateList(Delegate, list):

    def __init__(self, value):
        list.__init__([])
        for i in value:
            if isinstance(i, Delegate):
                self.append(i)
            else:
                self.append(choose_delegate(i))

    def update(self, state):
        for i in range(len(state)):
            if i < len(self) and isinstance(self[i], Delegate):
                self[i] = self[i].update(state[i])
            else:
                self.append(choose_delegate(state[i]))
        return self

    def __hash__(self):
        return hash(tuple(self))


class DelegateTuple(Delegate, tuple):
    def __init__(self, value):
        tuple.__init__((i if isinstance(i, Delegate) else choose_delegate(i) for i in value))

    def update(self, state):
        return DelegateTuple(state)

    def __hash__(self):
        return hash(tuple(self))


class DelegateSet(Delegate, set):
    def __init__(self, value):
        super().__init__()
        for i in value:
            self.add(i if isinstance(i, Delegate) else choose_delegate(i))

    def update(self, state):
        for i in state:
            self.add(i if isinstance(i, Delegate) else choose_delegate(i))
        return self

    def __hash__(self):
        return hash(tuple(self))


class DelegateDict(Delegate, dict):

    def __init__(self, value):
        dict.__init__({})
        for k in value:
            if k != "__type__":
                if isinstance(value[k], Delegate):
                    self[k] = value[k]
                else:
                    self[k] = choose_delegate(value[k])

    def update(self, state):
        for k in state:
            if k in self:
                self[k] = self[k].update(state[k])
            else:
                self[k] = choose_delegate(state[k])
        return self

    def __hash__(self):
        return hash(tuple(self.keys()))


class Object(DelegateDict):
    def __init__(self, value):
        DelegateDict.__init__(self, value)
        if "__type__" in value:
            self.__type__ = value["__type__"]

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"'{self.__type__}' object has no attribute '{name}'")

    def update(self, state):
        for k in state:
            if k != "__type__":
                if k in self and isinstance(self[k], Delegate):
                    self[k] = self[k].update(state[k])
                else:
                    self[k] = choose_delegate(state[k])
        return self


class AutoEntityObject(Object, IStateEntity):

    def __init__(self, state):
        Object.__init__(self, state)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityObject(state)


class AutoEntityBool(DelegateBool, IStateEntity):
    def __init__(self, value):
        DelegateBool.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityBool(state)


class AutoEntityInt(DelegateInt, IStateEntity):

    def __init__(self, value):
        DelegateInt.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityInt(state)


class AutoEntityFloat(DelegateFloat, IStateEntity):

    def __init__(self, value):
        DelegateFloat.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityFloat(state)


class AutoEntityComplex(DelegateComplex, IStateEntity):

    def __init__(self, value):
        DelegateComplex.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityComplex(state)


class AutoEntityStr(DelegateStr, IStateEntity):

    def __init__(self, value):
        DelegateStr.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityStr(state)


class AutoEntityList(DelegateList, IStateEntity):

    def __init__(self, value):
        DelegateList.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityList(state)


class AutoEntityTuple(DelegateTuple, IStateEntity):

    def __init__(self, value):
        DelegateTuple.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityTuple(state)


class AutoEntitySet(DelegateSet, IStateEntity):

    def __init__(self, value):
        DelegateSet.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntitySet(state)


class AutoEntityDict(DelegateDict, IStateEntity):

    def __init__(self, value):
        DelegateDict.__init__(self, value)

    @staticmethod
    def build(state) -> IStateEntity:
        return AutoEntityDict(state)


class AutoEntityManager(EntityManager):
    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        if game_element_state.type == "unknown":
            if isinstance(game_element_state.state, int):
                return AutoEntityInt.build(game_element_state.state)
            elif isinstance(game_element_state.state, bool):
                return AutoEntityBool.build(game_element_state.state)
            elif isinstance(game_element_state.state, dict):
                return AutoEntityDict.build(game_element_state.state)
            elif isinstance(game_element_state.state, str):
                return AutoEntityStr.build(game_element_state.state)
            elif isinstance(game_element_state.state, float):
                return AutoEntityFloat.build(game_element_state.state)
            elif isinstance(game_element_state.state, list):
                return AutoEntityList.build(game_element_state.state)
            elif isinstance(game_element_state.state, tuple):
                return AutoEntityTuple.build(game_element_state.state)
            elif isinstance(game_element_state.state, set):
                return AutoEntitySet.build(game_element_state.state)
            elif isinstance(game_element_state.state, complex):
                return AutoEntityComplex.build(game_element_state.state)
            else:
                raise ValueError(f"Unknown type {type(game_element_state.state)}")
        return AutoEntityObject.build(game_element_state.state)

    def __getattr__(self, item):
        if item in self._entities:
            return self._entities[item]
        raise AttributeError
