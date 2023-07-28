import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from xumes.training_module import observation, reward, terminated, action, config

#from games_examples.super_mario.classes.Level import nb_entites


@config
def train_impl(game_context):

    game_context.player_x, game_context.coins, game_context.points, game_context.player_state = 0, 0, 0, 0
    game_context.actions = ["nothing", "nothing", "nothing", "nothing"]

    dct = {
        'mario_rect': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'mario_powerUpState': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'ending_level': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_coins': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_points': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
    }

    for idx in range(1):
        dct[f'entity_{idx}_name'] = spaces.Discrete(10)
        dct[f'entity_{idx}_type'] = spaces.Discrete(3)
        dct[f'entity_{idx}_position'] = spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)
        dct[f'entity_{idx}_alive'] = spaces.Discrete(2)
        dct[f'entity_{idx}_active'] = spaces.Discrete(2)
        dct[f'entity_{idx}_bouncing'] = spaces.Discrete(2)
        dct[f'entity_{idx}_onGround'] = spaces.Discrete(2)

    game_context.observation_space = spaces.Dict(dct)
    game_context.action_space = spaces.MultiBinary(4)
    game_context.max_episode_length = 2000
    game_context.total_timesteps = int(50000)
    game_context.algorithm_type = "MultiInputPolicy"
    game_context.algorithm = stable_baselines3.PPO
    game_context.random_reset_rate = 0.0

@observation
def train_impl(game_context):
    dct = {
        'mario_rect': np.array(game_context.mario.rect),
        'mario_powerUpState': np.array([game_context.mario.powerUpState]),
        'ending_level': np.array([game_context.mario.ending_level]),
        'dashboard_coins': np.array([game_context.mario.dashboard.coins]),
        'dashboard_points': np.array([game_context.mario.dashboard.points])
    }

    for idx, entity in enumerate(game_context.mario.levelObj.entityList):
        dct[f'entity_{idx}_name'] = np.array([entity.name])
        dct[f'entity_{idx}_type'] = np.array([entity.type])
        dct[f'entity_{idx}_position'] = np.array([entity.position.x, entity.position.y])
        dct[f'entity_{idx}_alive'] = np.array([entity.alive])
        dct[f'entity_{idx}_active'] = np.array([entity.active])
        dct[f'entity_{idx}_bouncing'] = np.array([entity.bouncing])
        dct[f'entity_{idx}_onGround'] = np.array([entity.onGround])

    return dct


@reward
def train_impl(game_context):
    reward = 0
    if game_context.mario.dashboard.coins > game_context.coins:
        reward += 0.6
    if game_context.mario.dashboard.points > game_context.points:
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
    term = game_context.game.terminated or game_context.mario.rect[0] >= 448
    return term


@action
def train_impl(game_context, raw_actions):
    moves = [["nothing", "space"], ["nothing", "up"], ["nothing", "left"], ["nothing", "right"]]
    game_context.actions = [moves[0][int(raw_actions[0])], moves[1][int(raw_actions[1])],
                            moves[2][int(raw_actions[2])], moves[3][int(raw_actions[3])]]
    return game_context.actions




