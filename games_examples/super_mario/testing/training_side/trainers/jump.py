import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from xumes.training_module import observation, reward, terminated, action, config


@config
def train_impl(game_context):

    game_context.player_x, game_context.coins, game_context.points, game_context.player_state = 0, 0, 0, 0
    game_context.actions = ["nothing", "nothing"]

    game_context.observation_space = spaces.Dict({
        'mario_rect': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'mario_powerUpState': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'ending_level': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_coins': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_points': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
    }),

    game_context.action_space = spaces.MultiDiscrete([3, 2]),
    game_context.max_episode_length = 2000,
    game_context.total_timesteps = int(50000),
    game_context.algorithm_type = "MultiInputPolicy",
    game_context.algorithm = stable_baselines3.PPO,
    game_context.random_reset_rate = 0.0

@observation
def train_impl(game_context):
    return {
        'mario_rect': np.array([game_context.mario.rect]),
        'mario_powerUpState': np.array([game_context.mario.powerUpState]),
        'ending_level': np.array([game_context.mario.ending_level]),
        'dashboard_coins': np.array([game_context.mario.dashboard[0]]),
        'dashboard_points': np.array([game_context.mario.dashboard[1]]),
    }


@reward
def train_impl(game_context):
    reward = 0
    if game_context.mario.dashboard[0] > game_context.coins:
        reward += 0.6
    if game_context.mario.dashboard[1] > game_context.points:
        reward += 0.5
    if game_context.game.terminated or (game_context.player_state > game_context.mario.powerUpState):
        reward -= 5
    if game_context.ending_level:
        reward += 5

    xDiff = game_context.mario.rect[0] - game_context.player_x
    if xDiff >= 8:
        reward += 1
    elif xDiff > 0:
        reward += 0.5
    elif xDiff >= -8:
        reward -= 1.0
    else:
        reward -= 1.5

    return reward


@terminated
def train_impl(game_context):
    term = game_context.game.terminated or game_context.mario.rect.x >= 448
    return term


@action
def train_impl(game_context, raw_actions):
    directions = ["nothing", "left", "right"]
    positions = ["nothing", "space"]
    game_context.actions = [directions[raw_actions[0]], positions[raw_actions[1]]]
    return game_context.actions


