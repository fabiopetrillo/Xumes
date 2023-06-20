from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final, List, TypeVar

from xumes.game_module.implementations.rest_impl.json_game_state_observer import JsonGameStateObserver
from xumes.game_module.state_observable import StateObservable, State, GameStateObservable

OBJ = TypeVar("OBJ")


# decorator for notifying observers
def update_state_decorator(func, name):
    def wrapper(self, *arg, **kw):
        res = func(self, *arg, **kw)
        self.update_state(name)
        return res

    return wrapper


class _TestRunner(StateObservable, ABC):
    """
       The `_TestRunner` class is an abstract base class for implementing game test loop functionality and managing game state.

       Attributes:
           _test_client: The client object associated with the test runner.
           _game_state: The current state of the game.

       Methods:
           update_state(state): Notifies changes in the game state. This method should be used when overloading game methods.
           set_client(client): Sets the client object for the test runner.
           run_test(): Runs a game loop without rendering. The game loop should start with `self.test_client.wait()`.
           run_test_render(): Runs a game loop with rendering. The game loop should start with `self.test_client.wait()`.
           random_reset(): Performs a random reset in the game, starting from a random state.
           reset(): Performs a reset from the beginning of the game.
           delete_screen(): Deletes the screen if the game engine supports it.
       """

    def __init__(self, game_loop_object, observers=None):
        if observers is None:
            observers = [JsonGameStateObserver.get_instance()]
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

    @final
    def bind(self, observable_object: OBJ, name: str, state:  List[State] | State | str | List[str] | None = None) -> GameStateObservable:
        """
        Add an observable object to the test runner.
        :param observable_object: the observable object to add.
        :param name: the name of the observable object.
        :param state: the state of the observable object.
        """
        return GameStateObservable(observable_object, name, self.observers, state)

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
