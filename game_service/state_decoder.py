from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from game_service.state_observable import StateObservable

T = TypeVar('T')


class StateDecoder(Generic[T], ABC):

    def __init__(self, obs: Type[StateObservable]):
        self._observable = obs

    @abstractmethod
    def state(self):
        pass
