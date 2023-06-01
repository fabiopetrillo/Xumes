import gymnasium as gym

from gymnasium import Space
from gymnasium.core import ObsType
from gymnasium.experimental.functional import ActType

from framework.training_service_module.trainer import _Trainer


class StableBaselinesTrainer(_Trainer):

    def __init__(self,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm):
        super().__init__()
        self.env = gym.make(
            id="gym_env",
            max_episode_steps=max_episode_length,
            trainer=self,
            observation_space=observation_space,
            action_space=action_space
        )
        self.algorithm = algorithm
        self.algorithm_type = algorithm_type
        self.total_timesteps = total_timesteps
        self.model = None

    def train(self):
        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1).learn(self.total_timesteps)

    def save(self, path):
        self.model.save(path)
