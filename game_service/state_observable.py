from typing import Dict

from game_service.state_observer import StateObserver


class StateObservable:

    def __init__(self, observable_object, state_decoder_class):
        self._observers = []
        self._state_decoder = state_decoder_class(self)
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

    def state(self) -> Dict:
        if self._state_decoder:
            return self._state_decoder.state()
        else:
            raise Exception("State decoder not defined!")

    def get_observable_object(self):
        return self._observable_object
