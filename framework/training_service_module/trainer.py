from abc import abstractmethod
from typing import final


class _Trainer:

    def __init__(self):
        self._training_service = None

    @final
    def set_training_service(self, training_service):
        self._training_service = training_service

    @final
    def push_action(self, action):
        self._training_service.push_action(action)

    @final
    def get_obs(self):
        return self._training_service.get_obs()

    @final
    def reset(self):
        self._training_service.reset()

    @final
    def reward(self, obs):
        return self._training_service.reward(obs)

    @final
    def done(self):
        return self._training_service.done()

    @abstractmethod
    def train(self):
        pass
