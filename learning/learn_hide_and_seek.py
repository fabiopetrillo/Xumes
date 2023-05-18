import gym_pygame
import gymnasium as gym

from stable_baselines3 import PPO

from envs.hide_and_seek.params import ENV_NAME, TEST_NAME

env = gym.make(f"gym_pygame/{ENV_NAME}")

time_steps = int(2e4)

PPO('MultiInputPolicy', env, learning_rate=1e-3, verbose=1).load("./model/HNS-v0-second_level.zip", env).learn(total_timesteps=time_steps).save(
    f"./model/{ENV_NAME}-{TEST_NAME}")

env.close()

