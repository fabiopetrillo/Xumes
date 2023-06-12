from abc import abstractmethod, ABC
from typing import TypeVar, final

from xumes.training_module.entity_manager import EntityManager
from xumes.training_module.i_communication_service_training import ICommunicationServiceTraining

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
        """
        Implementation of the training algorithm.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def load(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def play(self, timesteps: int):
        """
        Use the algorithm not in training mode.
        :param timesteps: Number maximum of step (action to perform).
        """
        raise NotImplementedError

    @final
    def random_reset(self):
        self._communication_service.push_event("random_reset")

    @final
    def reset(self):
        self._communication_service.push_event("reset")

    @final
    def push_actions(self, actions):
        self._communication_service.push_actions(actions)

    @final
    def retrieve_state(self) -> None:
        """
        Call the game service and update the state.
        """
        for state in self._communication_service.get_states():
            self._entity_manager.convert(state)

    @final
    @property
    def game_state(self):
        return self._entity_manager.game_state

    @final
    def get_entity(self, name: str):
        return self._entity_manager.get(name)


class MarkovTrainingService(TrainingService, ABC): # TODO Move class to implementations folder 

    @abstractmethod
    def get_obs(self) -> OBST:
        """
        Method needed in the Markov Decision Process.
        Convert game state to observation.
        """
        raise NotImplementedError

    @abstractmethod
    def reward(self) -> float:
        """
        Method needed in the Markov Decision Process.
        Convert game state to reward.
        """
        raise NotImplementedError

    @abstractmethod
    def push_raw_actions(self, actions):
        """
        Method needed in the Markov Decision Process.
        Convert actions (ex: list of int), to list of str.
        :param actions: Any type of actions.
        """
        raise NotImplementedError

    @abstractmethod
    def terminated(self) -> bool:
        """
        Method needed in the Markov Decision Process.
        Get if the episode is terminated from the game state.
        """
        raise NotImplementedError
