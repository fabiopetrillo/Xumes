import gym_pygame
import gymnasium as gym

from stable_baselines3 import PPO, A2C

from envs.hide_and_seek.params import ENV_NAME, TEST_NAME

env = gym.make(f"gym_pygame/{ENV_NAME}")

time_steps = int(4e4)

PPO('MultiInputPolicy', env, learning_rate=1e-3, verbose=1).learn(total_timesteps=time_steps).save(
    f"./model/{ENV_NAME}-{TEST_NAME}")

env.close()

