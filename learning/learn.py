import random

import numpy as np
import torch
import gymnasium as gym
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from envs.v0.params import ENV_NAME, TEST_NAME
from learning.reinforce import REINFORCE


env = gym.make(f"gym_pygame/{ENV_NAME}")
wrapped_env = gym.wrappers.RecordEpisodeStatistics(env, 50)  # Records episode-reward

total_num_episodes = int(3e4)  # Total number of episodes

# Observation-space of InvertedPendulum-v4 (4)
obs_space_dims = 0

for space in env.observation_space:
    obs_space_dims += env.observation_space[space].shape[0]

action_space_dims = 1

# set seed
seed = 42
torch.manual_seed(seed)
random.seed(seed)
np.random.seed(seed)

agent = REINFORCE(obs_space_dims, action_space_dims)
reward_over_episodes = []
distance_over_episodes = []

best_average_reward = [-1, None]

for episode in range(total_num_episodes+1):
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
    distance_over_episodes.append(info['distance'])
    agent.update()
    if episode % 1000 == 0:
        avg_reward = int(np.mean(wrapped_env.return_queue))
        if avg_reward >= best_average_reward[0]:
            best_average_reward[0] = avg_reward
            best_average_reward[1] = agent.net.state_dict()
        print("Episode:", episode, "Average Reward:", avg_reward)


# Save graph for the distances
df1 = pd.DataFrame([distance_over_episodes]).melt()
df1.rename(columns={"variable": "episodes", "value": "distance"}, inplace=True)
sns.set(style="darkgrid", context="talk", palette="rainbow")

plt.figure(figsize=(18, 8))
sns.lineplot(x="episodes", y="distance", data=df1, sizes=(15, 8)).set(
    title=f"{ENV_NAME} {TEST_NAME} distance"
)
plt.savefig(f"./graphs/{ENV_NAME}-{TEST_NAME}-distance.png")
plt.show()

# Save graph for the rewards
rewards_to_plot = [[reward[0] for reward in reward_over_episodes]]
df1 = pd.DataFrame(rewards_to_plot).melt()
df1.rename(columns={"variable": "episodes", "value": "reward"}, inplace=True)
sns.set(style="darkgrid", context="talk", palette="rainbow")
plt.figure(figsize=(18, 8))
sns.lineplot(x="episodes", y="reward", data=df1).set(
    title=f"{ENV_NAME} {TEST_NAME} reward"
)
plt.savefig(f"./graphs/{ENV_NAME}-{TEST_NAME}-reward.png")
plt.show()


# Save the model
agent.net.save()
print(f"Saving best average reward {best_average_reward[0]}")
agent.net.save_dict(best_average_reward[1])

env.close()
