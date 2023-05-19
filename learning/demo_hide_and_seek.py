import gym_pygame
import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

from envs.hide_and_seek.params import ENV_NAME, TEST_NAME

env = gym.make(f"gym_pygame/{ENV_NAME}", render_mode="human")
model = PPO('MultiInputPolicy', env, verbose=1)
model = model.load(f"./model/{ENV_NAME}-{TEST_NAME}")
# Evaluate the agent
# mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
# print(mean_reward, std_reward)
# Enjoy trained agent
obs, info = env.reset()
for i in range(10000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    if done or truncated:
        obs, info = env.reset()
    env.render()
