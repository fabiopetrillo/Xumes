# Create and wrap the environment
import random
import gym_pygame

import numpy as np
import torch
import gymnasium as gym

from learning.reinforce import REINFORCE

env = gym.make("gym_pygame/RLFlappy-v0")
wrapped_env = gym.wrappers.RecordEpisodeStatistics(env, 50)  # Records episode-reward

total_num_episodes = int(5e4)  # Total number of episodes

# Observation-space of InvertedPendulum-v4 (4)
obs_space_dims = 0
for space in env.observation_space:
    obs_space_dims += env.observation_space[space].shape[0]

# Action-space of InvertedPendulum-v4 (1)
action_space_dims = 2

# set seed
seed = 42
torch.manual_seed(seed)
random.seed(seed)
np.random.seed(seed)

# Reinitialize agent every seed
agent = REINFORCE(obs_space_dims, action_space_dims)
reward_over_episodes = []

for episode in range(total_num_episodes):
    # gymnasium v26 requires users to set seed while resetting the environment
    obs, info = wrapped_env.reset(seed=seed)

    done = False
    while not done:
        obs_array = []
        obs_array.append(obs['speedup'])
        obs_array.extend(obs['lidar'])
        action = agent.sample_action(obs_array)

        # Step return type - `tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]`
        # These represent the next observation, the reward from the step,
        # if the episode is terminated, if the episode is truncated and
        # additional info from the step
        obs, reward, terminated, truncated, info = wrapped_env.step(action)
        agent.rewards.append(reward)

        # End the episode when either truncated or terminated is true
        #  - truncated: The episode duration reaches max number of timesteps
        #  - terminated: Any of the state space values is no longer finite.
        done = terminated

    reward_over_episodes.append(wrapped_env.return_queue[-1])
    agent.update()

    if episode % 1000 == 0:
        avg_reward = int(np.mean(wrapped_env.return_queue))
        print("Episode:", episode, "Average Reward:", avg_reward)

env.close()
env = gym.make("gym_pygame/RLFlappy-v0", render_mode="human")
for episode in range(total_num_episodes):
    # gymnasium v26 requires users to set seed while resetting the environment
    obs, info = env.reset(seed=seed)

    done = False
    while not done:
        obs_array = []
        obs_array.append(obs['speedup'])
        obs_array.extend(obs['lidar'])
        action = agent.sample_action(obs_array)

        # Step return type - `tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]`
        # These represent the next observation, the reward from the step,
        # if the episode is terminated, if the episode is truncated and
        # additional info from the step
        obs, reward, terminated, truncated, info = env.step(action)
        agent.rewards.append(reward)

        # End the episode when either truncated or terminated is true
        #  - truncated: The episode duration reaches max number of timesteps
        #  - terminated: Any of the state space values is no longer finite.
        done = terminated
