from abc import ABC, abstractmethod
from typing import Dict

from game_service.state_observer import StateObserver


class StateObservable(ABC):

    def __init__(self):
        self._observers = []
        self._state_decoder = self.set_state_decoder()

    @abstractmethod
    def set_state_decoder(self):
        raise NotImplementedError

    def attach(self, observer: StateObserver) -> None:
        self._observers.append(observer)
        observer.update(self)

    def detach(self, observer: StateObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def state(self) -> Dict:
        if self._state_decoder:
            return self._state_decoder.state()
        else:
            raise Exception("State decoder not defined!")
