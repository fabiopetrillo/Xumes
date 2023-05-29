from abc import ABC, abstractmethod
from typing import TypeVar, final

from game_service.game_element_state import GameElementState
from game_service.state_observable import StateObservable

GLST = TypeVar("GLST")
GLOBJ = TypeVar("GLOBJ")


class _TestRunner(StateObservable[GLOBJ, GLST], ABC):

    def __init__(self, game_loop_object: GLOBJ):
        super().__init__(game_loop_object)
        self._test_client = None
        self._game_state = "playing"
        self._game_loop_object = game_loop_object

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

    @final
    @property
    def game_loop(self):
        return self._game_loop_object

    @abstractmethod
    def run_test(self) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def quit_screen(self) -> None:
        pass


class JsonTestRunner(_TestRunner, ABC):

    def state(self):
        return GameElementState({
            "state": self._game_state
        })
