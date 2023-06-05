import gym_pygame
from stable_baselines3 import PPO

import gymnasium as gym
from gym_envs.flappy_bird.params import ENV_NAME, TEST_NAME


env = gym.make(f"gym_pygame/{ENV_NAME}")

time_steps = int(2e4)

PPO('MultiInputPolicy', env, verbose=1).learn(total_timesteps=time_steps).save(
    f"./model/{ENV_NAME}-{TEST_NAME}")

env.close()