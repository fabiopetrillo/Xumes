from abc import ABC, abstractmethod
from typing import final

from xumes.game_module.state_observable import StateObservable


class _TestRunner(StateObservable, ABC):

    def __init__(self, game_loop_object, observers):
        self._test_client = None
        self._game_state = "playing"
        super().__init__(observable_object=game_loop_object, observers=observers, name="test_runner")

    @final
    def update_state(self, state) -> None:
        """
        Method used to notify changes in the game state,
        use that method when overloading game methods.
        :param state: a game state (ex: "alive", "dead").
        """
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
        """
        Run a game loop without rendering.\n
        The game loop has to start with : self.test_client.wait()
        """
        raise NotImplementedError

    @abstractmethod
    def run_test_render(self) -> None:
        """
        Run a game loop with rendering.\n
        The game loop has to start with : self.test_client.wait()
        """
        raise NotImplementedError

    @abstractmethod
    def random_reset(self) -> None:
        """
        Perform a random reset in the game. A random reset,
        is a reset from a random state of the game and not from the beginning.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        Perform a reset from the beginning of the game.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_screen(self) -> None:
        """
        If the game engine able it, implement a way to delete the
        screen.
        """
        raise NotImplementedError



