from abc import ABC, abstractmethod
from typing import final

from framework.game_service_module.game_element_state import GameElementState
from framework.game_service_module.state_observable import StateObservable


class _TestRunner(StateObservable, ABC):

    def __init__(self, game_loop_object, observers):
        self._test_client = None
        self._game_state = "playing"
        super().__init__(observable_object=game_loop_object, observers=observers, name="test_runner")

    @final
    def update_state(self, state) -> None:
        self._game_state = state
        self.notify()

    @property
    @final
    def test_client(self):
        return self._test_client

    @final
    def set_client(self, client):
        self._test_client = client

    @abstractmethod
    def run_test(self) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def delete_screen(self) -> None:
        pass


class JsonTestRunner(_TestRunner, ABC):

    def state(self):
        return GameElementState({
            "state": self._game_state
        })
