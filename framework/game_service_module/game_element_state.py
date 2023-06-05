from typing import Generic, TypeVar

ST = TypeVar("ST")


class GameElementState(Generic[ST]):

    def __init__(self, state_obj: ST):
        self._state: ST = state_obj

    @property
    def state(self) -> ST:
        return self._state
