from typing import Generic, TypeVar

ST = TypeVar("ST")


class GameElementState(Generic[ST]):

    def __init__(self, name: str, element_type: str, state_obj: ST):
        self._state: ST = state_obj
        self._type = element_type
        self._name = name

    @property
    def state(self) -> ST:
        return self._state

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self):
        return self._type
