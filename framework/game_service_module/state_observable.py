from abc import ABC, abstractmethod
from typing import TypeVar, Generic, final, List

from framework.game_service_module.game_element_state import GameElementState
from framework.game_service_module.i_game_state_observer import IGameStateObserver

OBJ = TypeVar("OBJ")
ST = TypeVar("ST")


class StateObservable(Generic[OBJ, ST], ABC):

    def __init__(self, observable_object: OBJ, observers: List[IGameStateObserver], name: str):
        self._observers = []
        self._object = observable_object
        self._name = name
        for observer in observers:
            self.attach(observer)

    @final
    def attach(self, observer: IGameStateObserver) -> None:
        """
        Attach method of the observable.
        :param observer: GameStateObserver implementation.
        """
        self._observers.append(observer)

    @final
    def detach(self, observer: IGameStateObserver) -> None:
        """
        Detach method of the observable.
        :param observer: GameStateObserver implementation.
        """
        if observer in self._observers:
            observer.remove_state(self)
            self._observers.remove(observer)

    @final
    def detach_all(self):
        """
        Detach every observer, we used this method when we want to
        destroy the object.
        """
        if self._observers is not None and self._observers:
            for observer in self._observers:
                observer.remove_state(self)

        self._observers.clear()

    @final
    def notify(self):
        """
        Notify method of the observable.
        """
        if self._observers is not None and self._observers:
            for observer in self._observers:
                observer.update_state(self)

    @abstractmethod
    def state(self) -> GameElementState[ST]:
        """
        Give a representation method of a game element state.
        Mandatory for every class we want to observe.
        """
        raise NotImplementedError

    @property
    @final
    def name(self) -> str:
        return self._name

    @final
    @property
    def observers(self):
        return self._observers

    @final
    @property
    def object(self):
        return self._object

