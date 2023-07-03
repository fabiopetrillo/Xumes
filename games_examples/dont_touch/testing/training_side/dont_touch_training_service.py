import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces
from xumes.training_module import StableBaselinesTrainer, EntityManager

from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.testing.training_side.entities.dont_touch_entity_manager import DontTouchEntityManager
from src.xumes.training_module.implementations.mq_impl.communication_service_training_mq import \
    CommunicationServiceTrainingMq
from src.xumes.training_module.implementations.rest_impl.json_game_element_state_converter import \
    JsonGameElementStateConverter
from src.xumes.training_module.training_service import OBST


class DontTouchTrainingService(StableBaselinesTrainer):

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

    def convert_obs(self) -> OBST:

        player = self.get_entity("player")
        scoreboard = self.get_entity("scoreboard")
        left_hand = self.get_entity("left_hand")
        right_hand = self.get_entity("right_hand")

        return {
            'player_x' : np.array([player.position[0]]),
            'player_y' : np.array([player.position[0]]),
            'left_hand_x': np.array([left_hand.position[0]]),
            'left_hand_y': np.array([left_hand.position[1]]),
            'left_hand_speed': np.array([left_hand.speed]),
            'right_hand_x': np.array([right_hand.position[0]]),
            'right_hand_y': np.array([right_hand.position[1]]),
            'right_hand_speed': np.array([right_hand.speed]),
            'scoreboard_current_score': np.array([scoreboard.current_score]),
            'scoreboard_max_score': np.array([scoreboard.max_score])
        }

    def convert_reward(self) -> float:
        reward = 0

        player = self.get_entity("player")
        scoreboard = self.get_entity("scoreboard")
        left_hand = self.get_entity("left_hand")
        right_hand = self.get_entity("right_hand")

        if player.position[1] < Config.HEIGHT - 20:
            reward += 0.2
        if scoreboard.current_score > self.score:
            reward += 5
            self.score = scoreboard.currend_score
        if scoreboard.current_score >= scoreboard.max_score:
            reward += 10
        if self.game.terminated:
            reward -= 5

        if left_hand.position[1] > right_hand.position[1]:
            if left_hand.position[0] < player.poisition[0]:
                reward += 0.1
        else:
            if right_hand.position[0] > player.poisition[0]:
                reward += 0.1

        return reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        direction = ["nothing", "left", "right"]
        position = ["nothing", "up", "down"]
        self.actions = [direction[raws_actions[0]], position[raws_actions[1]]]
        return self.actions

if __name__ == "__main__":

    dct = {
        'player_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'player_y' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'left_hand_x' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'left_hand_y' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'left_hand_speed' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_x' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_y' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_speed' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'scoreboard_current_score' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'scoreboard_max_score' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,))

    }

    training_service = DontTouchTrainingService(
        entity_manager=DontTouchEntityManager(
            JsonGameElementStateConverter()
        ),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(dct),
        action_space=spaces.MultiDiscrete([3, 3]),
        max_episode_length=2000,
        total_timesteps=200000,
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



