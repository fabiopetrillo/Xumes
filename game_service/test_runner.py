from abc import ABC, abstractmethod
from typing import TypeVar, final

from game_service.game_element_state import GameElementState
from game_service.state_observable import StateObservable

GameLoopT = TypeVar("GameLoopT")


class TestRunner(StateObservable, ABC):
    class GameLoop:
        pass

    def __init__(self):
        super().__init__(TestRunner.GameLoop())
        self._test_client = None
        self._state = "playing"

    @final
    def update_state(self, state) -> None:
        self._state = state
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
    def quit_screen(self) -> None:
        pass


class JsonTestRunner(TestRunner, ABC):

    def state(self):
        return GameElementState({
            "state": self._state
        })
