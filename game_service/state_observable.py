from abc import ABC, abstractmethod
from typing import Dict

from game_service.state_observer import StateObserver


class StateObservable(ABC):

    def __init__(self, observable_object):
        self._observers = []
        self._observable_object = observable_object

    def attach(self, observer: StateObserver) -> None:
        self._observers.append(observer)
        observer.update(self)

    def detach(self, observer: StateObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    @abstractmethod
    def state(self) -> Dict:
        pass

    @property
    def object(self):
        return self._observable_object
