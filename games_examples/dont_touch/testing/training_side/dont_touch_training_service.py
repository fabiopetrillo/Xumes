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


