import logging
import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from xumes.training_module import StableBaselinesTrainer, JsonGameElementStateConverter, CommunicationServiceTrainingMq, AutoEntityManager


class SuperMarioTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager,
                 communication_service,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm,
                 random_reset_rate: float):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm, random_reset_rate)

        self.player_x, self.coins, self.points, self.player_state = 0, 0, 0, 0
        self.actions = ["nothing", "nothing"]

    def convert_obs(self):

        return {
            'mario_rect': np.array([self.mario.rect]),
            'mario_powerUpState': np.array([self.mario.powerUpState]),
            'ending_level': np.array([self.mario.ending_level]),
            'dashboard_coins': np.array([self.mario.dashboard[0]]),
            'dashboard_points': np.array([self.mario.dashboard[1]]),
        }

    def convert_reward(self):

        reward = 0

        if self.mario.dashboard[0] > self.coins:
            reward += 0.6
        if self.mario.dashboard[1] > self.points:
            reward += 0.5
        if self.game.terminated or (self.player_state > self.mario.powerUpState):
            reward -= 5
        if self.ending_level:
            reward += 5

        xDiff = self.mario.rect[0] - self.player_x
        if xDiff >= 8:
            reward += 1
        elif xDiff > 0:
            reward += 0.5
        elif xDiff >= -8:
            reward -= 1.0
        else:
            reward -= 1.5

        return reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raw_actions):
        directions = ["nothing", "left", "right"]
        positions = ["nothing", "up", "space"]
        self.actions = [directions[raw_actions[0]], positions[raw_actions[1]]]
        return self.actions


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    training_service = SuperMarioTrainingService(
        entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict({
                'mario_rect': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
                'mario_powerUpState': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
                'ending_level': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
                'dashboard_coins': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
                'dashboard_points': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
        }),
        action_space=spaces.MultiDiscrete([3, 3]),
        max_episode_length=2000,
        total_timesteps=int(2e5),
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO,
        random_reset_rate=0.0
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            training_service.train(save_path="./models", log_path="./logs", test_name="test")
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/best_model.zip")
            training_service.play(100000)
