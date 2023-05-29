from abc import ABC, abstractmethod
from typing import TypeVar, Generic, final

from game_service.game_element_state import GameElementState
from game_service.game_state_observer import IGameStateObserver

OBJ = TypeVar("OBJ")
ST = TypeVar("ST")


class StateObservable(Generic[OBJ, ST], ABC):

    def __init__(self, observable_object: OBJ):
        self._observers = []
        self._observable_object: OBJ = observable_object

    @final
    def attach(self, observer: IGameStateObserver) -> None:
        self._observers.append(observer)
        observer.update_state(self)

    @final
    def detach(self, observer: IGameStateObserver) -> None:
        if observer in self._observers:
            observer.remove_state(self)
            self._observers.remove(observer)

    @final
    def detach_all(self):
        for observer in self._observers:
            observer.remove_state(self)

        self._observers.clear()

    @final
    def notify(self):
        for observer in self._observers:
            observer.update_state(self)

    @abstractmethod
    def state(self) -> GameElementState[ST]:
        pass

    @property
    @final
    def object(self):
        return self._observable_object
