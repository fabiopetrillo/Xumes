import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from framework.training_service_module.entity_manager import EntityManager
from framework.training_service_module.i_communication_service_training import ICommunicationServiceTraining
from framework.training_service_module.i_game_element_state_builder import JsonGameElementStateConverter
from framework.training_service_module.implementations.gym_impl.stable_baselines_trainer import StableBaselinesTrainer, \
    OBST
from framework.training_service_module.implementations.mq_impl.communication_service_training_mq import \
    CommunicationServiceTrainingMq
from games_examples.flappy_bird.params import LIDAR_MAX_DIST
from games_examples.flappy_bird.testing.training_side.entities.flappy_bird_entity_manager import FlappyBirdEntityManager
from games_examples.flappy_bird.testing.training_side.helpers.lidar import Lidar


class FlappyBirdTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service: ICommunicationServiceTraining,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm)

        self.pipes = None
        self.bird = None
        self.lidar = None

    def convert_obs(self) -> OBST:
        if not self.pipes:
            self.pipes = self.get_entity("pipes")
        if not self.bird:
            self.bird = self.get_entity("bird")
        if not self.lidar and self.pipes and self.bird:
            self.lidar = Lidar(self.pipes, self.bird)

        self.lidar.reset()
        self.lidar.vision()
        lidar = [line.distance for line in self.lidar.sight_lines]
        return {"speedup": np.array([self.bird.speedup]), "lidar": np.array(lidar)}

    def convert_reward(self) -> float:
        if self.game_state == "reward":
            return 1
        elif self.game_state == "lose":
            return -1
        return 0

    def convert_terminated(self) -> bool:
        return self.game_state == "lose"

    def convert_actions(self, raws_actions) -> List[str]:
        if raws_actions == 1:
            return ["space"]
        return ["nothing"]


if __name__ == "__main__":
    training_service = FlappyBirdTrainingService(
        entity_manager=FlappyBirdEntityManager(
            JsonGameElementStateConverter()
        ),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict({
                "speedup": spaces.Box(-float('inf'), 300, shape=(1, ), dtype=float),
                "lidar": spaces.Box(0, LIDAR_MAX_DIST, shape=(7,), dtype=float),
        }),
        action_space=spaces.Discrete(2),
        max_episode_length=2000,
        total_timesteps=int(2e5),
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO
    )

    if len(sys.argv) == 2:
        if sys.argv[1] == "-train":
            training_service.train()
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model")
            training_service.play(100000)
