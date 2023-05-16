import gym_pygame
import gymnasium as gym

from stable_baselines3 import PPO

from envs.hide_and_seek.params import ENV_NAME, TEST_NAME


env = gym.make(f"gym_pygame/{ENV_NAME}", render_mode="human")

# Instantiate the agent
model = PPO('MultiInputPolicy', env, learning_rate=1e-3, verbose=2)
# Train the agent
model.learn(total_timesteps=int(2e5))
# Save the agent
model.save(f"./model/{ENV_NAME}-{TEST_NAME}")

env.close()

