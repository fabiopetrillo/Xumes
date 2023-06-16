import sys
#from abc import ABC
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces

from games_examples.batkill.testing.training_side.entites.batkiller_entity import BatKillerEntityManager
from games_examples.batkill.play import worldx, worldy
from xumes.training_module import StableBaselinesTrainer, CommunicationServiceTrainingMq, JsonGameElementStateConverter, \
    EntityManager


class BatKillerTrainingService(StableBaselinesTrainer):

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

    def convert_obs(self):

        player = self.get_entity("player")
        dct = {
            'player_x': np.array([(player.position.x / worldx) * 2 - 1]),
            'player_y': np.array([(player.position.x / worldy) * 2 - 1]),
            'player_direction': np.array([player.direction]),
            'player_attack': np.array([(
                                     player.attack_state / player.attack_duration) * 2 - 1]),
            'player_cooldown': np.array([(
                                       player.cool_down_state / player.cool_down_duration) * 2 - 1])
        }
        for idx in range(6):
            try:
                bat = self.get_entity("bat_" + str(idx))
            except KeyError:
                break
            if bat.dead is not True:
                dct[f'bat_{idx}_alive'] = np.array([1])
                dct[f'bat_{idx}_direction'] = np.array([bat.direction])
                dct[f'bat_{idx}_x'] = np.array([(bat.position.x / worldx) * 2 - 1])
                dct[f'bat_{idx}_speed'] = np.array([bat.speed])
                dct[f'bat_{idx}_distance_to_player'] = np.array([(bat.position.x - player.position.x) / worldx])
                if bat.direction == -1:
                    if bat.position.x > player.position.x:
                        bat_facing_player = 1
                    else:
                        bat_facing_player = -1
                else:
                    if bat.position.x < player.position.x:
                        bat_facing_player = 1
                    else:
                        bat_facing_player = -1
                if player.direction == -1:
                    if player.position.x > bat.position.x:
                        player_facing_bat = 1
                    else:
                        player_facing_bat = -1
                else:
                    if player.position_x < bat.position.x:
                        player_facing_bat = 1
                    else:
                        player_facing_bat = -1
                if player_facing_bat > 0:
                    attack_rect = player.attack_rect
                    if (
                            bat.collider_rect and
                            attack_rect.colliderect(bat.collider_rect) and
                            player.cool_down_state == 0 and
                            player.attack_state == 0
                    ):
                        bat_in_range = 1
                    else:
                        bat_in_range = -1
                else:
                    bat_in_range = -1

                dct[f'bat_{idx}_bat_facing_player'] = np.array([bat_facing_player])
                dct[f'bat_{idx}_player_facing_bat'] = np.array([player_facing_bat])
                dct[f'bat_{idx}_in_attack_range'] = np.array([bat_in_range])
            else:
                dct[f'bat_{idx}_alive'] = np.array([-1])
                dct[f'bat_{idx}_direction'] = np.array([0])
                dct[f'bat_{idx}_x'] = np.array([-1])
                dct[f'bat_{idx}_speed'] = np.array([0])
                dct[f'bat_{idx}_distance_to_player'] = np.array([0])
                dct[f'bat_{idx}_bat_facing_player'] = np.array([0])
                dct[f'bat_{idx}_player_facing_bat'] = np.array([0])
                dct[f'bat_{idx}_in_attack_range'] = np.array([0])

        return dct

    def convert_reward(self):

        player = self.get_entity("player")

        reward = 0

        if player.facing_nearest_bat is True:
            reward += 0.2

        for idx in range(6):
            try:
                bat = self.get_entity("bat_" + str(idx))
            except KeyError:
                break
            if bat.direction == -1:
                if bat.position.x < self.player.position.x:
                    reward += 0.1
            else:
                if bat.position.x > self.player.position.x:
                    reward += 0.1
            if player.attack_rect.colliderect(bat.collider_rect):
                reward += 5

        return reward






if __name__ == "__main__":
    training_service = BatKillerTrainingService(
        entity_manager=BatKillerEntityManager(
            JsonGameElementStateConverter()
        ),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(

        )
    )

    if len(sys.argv) == 2:
        if sys.argv[1] == "-train":
            training_service.train()
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model")
            training_service.play(100000)
