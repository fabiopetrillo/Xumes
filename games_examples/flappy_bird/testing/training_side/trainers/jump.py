import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces
from games_examples.flappy_bird.testing.training_side.helpers.lidar import Lidar
from games_examples.flappy_bird.params import LIDAR_MAX_DIST

from xumes.training_module import observation, reward, terminated, action, config


@config
def train_impl(train_context):
    train_context.lidar = None
    train_context.points = 0

    train_context.observation_space = spaces.Dict({
        "speedup": spaces.Box(-float('inf'), 300, shape=(1,), dtype=float),
        "lidar": spaces.Box(0, LIDAR_MAX_DIST, shape=(7,), dtype=int),
    })
    train_context.action_space = spaces.Discrete(2)
    train_context.max_episode_length = 2000
    train_context.total_timesteps = int(5e5)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO


@observation
def train_impl(train_context):
    if not train_context.lidar and train_context.pipe_generator and train_context.player:
        train_context.lidar = Lidar(train_context.pipe_generator, train_context.player)

    train_context.lidar.reset()
    train_context.lidar.vision()
    lidar = [line.distance for line in train_context.lidar.sight_lines]
    return {"speedup": np.array([train_context.player.speedup]), "lidar": np.array(lidar)}


@reward
def train_impl(train_context):
    if train_context.player.points > train_context.points:
        train_context.points = train_context.player.points
        return 1
    if train_context.game.terminated:
        return -1
    return 0


@terminated
def train_impl(train_context):
    term = train_context.game.terminated or train_context.player.points >= 2
    if term:
        train_context.lidar.reset()
        train_context.points = 0
    return term


@action
def train_impl(train_context, raw_actions):
    if raw_actions == 1:
        return ["space"]
    return ["nothing"]
