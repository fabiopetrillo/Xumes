from abc import abstractmethod
from typing import final, TypeVar, List

import gymnasium as gym

import xumes

from xumes.training_module.entity_manager import EntityManager
from xumes.training_module.i_communication_service_training import ICommunicationServiceTraining
from xumes.training_module.training_service import MarkovTrainingService

OBST = TypeVar("OBST")


class StableBaselinesTrainer(MarkovTrainingService):

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service: ICommunicationServiceTraining,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm):
        super().__init__(entity_manager, communication_service)
        self.env = gym.make(
            id="xumes-v0",
            max_episode_steps=max_episode_length,
            training_service=self,
            observation_space=observation_space,
            action_space=action_space
        )
        self.algorithm = algorithm
        self.algorithm_type = algorithm_type
        self.total_timesteps = total_timesteps
        self.model = None

    @final
    def train(self):
        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1).learn(self.total_timesteps)

    @final
    def save(self, path: str):
        self.model.save(path)

    @final
    def load(self, path: str):
        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1).load(path)

    @final
    def play(self, timesteps: int):
        obs, info = self.env.reset()
        for _ in range(timesteps):
            action, _states = self.model.predict(obs, deterministic=True)
            obs, reward, terminated, done, info = self.env.step(action)
            if done or terminated:
                self.env.reset(options={"not_random": True})

    @final
    def reward(self):
        return self.convert_reward()

    @final
    def terminated(self):
        return self.convert_terminated() or self._entity_manager.game_state == "reset" or self._entity_manager.game_state == "random_reset"

    @final
    def push_raw_actions(self, actions):
        self.push_actions(actions=self.convert_actions(actions))

    @final
    def get_obs(self) -> OBST:
        self.retrieve_state()
        return self.convert_obs()

    @abstractmethod
    def convert_obs(self) -> OBST:  # TODO Change pass to raise NotImplementedError
        pass

    @abstractmethod
    def convert_reward(self) -> float:
        pass

    @abstractmethod
    def convert_terminated(self) -> bool:
        pass

    @abstractmethod
    def convert_actions(self, raws_actions) -> List[str]:
        pass
