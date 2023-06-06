from abc import abstractmethod
from typing import final, TypeVar

OBST = TypeVar("OBST")


class _Trainer:

    def __init__(self):
        self._training_service = None

    @final
    def set_training_service(self, training_service):
        self._training_service = training_service

    @final
    def push_action(self, actions):
        self._training_service.push_action(actions)

    @final
    def get_obs(self) -> OBST:
        return self._training_service.get_obs()

    @final
    def random_reset(self):
        self._training_service.random_reset()

    @final
    def reset(self):
        self._training_service.reset()

    @final
    def reward(self):
        return self._training_service.reward()

    @final
    def terminated(self):
        return self._training_service.terminated()

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass

    @abstractmethod
    def play(self, timesteps: int):
        pass
