from abc import ABC, abstractmethod
from typing import Dict


class StateStrategy(ABC):

    @abstractmethod
    def state(self):
        pass


class JsonStateStrategy(StateStrategy, ABC):

    def state(self) -> Dict:
        pass
