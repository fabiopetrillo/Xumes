import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces
from xumes.training_module import StableBaselinesTrainer, EntityManager


class   DontTouchTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm)

        self.score = 0
        self.actions = ["nothing", "nothing"]

    def convert_reward(self) -> float:
        player = self.get_entity("player")
        scoreboard = self.get_entity("scoreboard")
        r = self.player.points
        if r > self.points:
            self.points = r
            return 1
        if self.game.terminated:
            return -1
        return 0

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        direction = ["nothing", "left", "right"]
        position = ["nothing", "up", "down"]
        self.actions = [direction[raws_actions[0]], position[raws_actions[1]]]
        return self.actions

