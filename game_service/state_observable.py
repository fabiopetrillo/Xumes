from abc import ABC, abstractmethod
from typing import TypeVar, Generic, final, List

from game_service.game_element_state import GameElementState
from game_service.game_state_observer import IGameStateObserver

OBJ = TypeVar("OBJ")
ST = TypeVar("ST")


class StateObservable(Generic[OBJ, ST], ABC):

    def __init__(self, observable_object: OBJ, observers: List[IGameStateObserver]):
        self._observers = []
        self._object = observable_object
        for observer in observers:
            self.attach(observer)

    @final
    def attach(self, observer: IGameStateObserver) -> None:
        self._observers.append(observer)

    @final
    def detach(self, observer: IGameStateObserver) -> None:
        if observer in self._observers:
            observer.remove_state(self)
            self._observers.remove(observer)

    @final
    def detach_all(self):
        if self._observers is not None and self._observers:
            for observer in self._observers:
                observer.remove_state(self)

        self._observers.clear()

    @final
    def notify(self):
        if self._observers is not None and self._observers:
            for observer in self._observers:
                observer.update_state(self)

    @abstractmethod
    def state(self) -> GameElementState[ST]:
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @final
    @property
    def observers(self):
        return self._observers

    @final
    @property
    def object(self):
        return self._object

