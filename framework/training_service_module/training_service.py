from abc import abstractmethod, ABC
from typing import TypeVar, final

from framework.training_service_module.entity_manager import EntityManager
from framework.training_service_module.i_communication_service_training import ICommunicationServiceTraining

OBST = TypeVar("OBST")


class TrainingService:

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service: ICommunicationServiceTraining,
                 ):
        self._entity_manager = entity_manager
        self._communication_service = communication_service

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

    @final
    def random_reset(self):
        self._communication_service.push_event("random_reset")

    @final
    def reset(self):
        self._communication_service.push_event("reset")

    @final
    @property
    def game_state(self):
        return self._entity_manager.game_state

    @final
    def get_entity(self, name: str):
        return self._entity_manager.get(name)


class MarkovTrainingService(TrainingService, ABC):

    @abstractmethod
    def get_obs(self) -> OBST:
        pass

    @abstractmethod
    def reward(self) -> float:
        pass

    @abstractmethod
    def push_action(self, actions):
        pass

    @abstractmethod
    def terminated(self) -> bool:
        pass
