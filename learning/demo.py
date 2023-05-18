import gym_pygame
import gymnasium as gym
from stable_baselines3 import PPO

from envs.v0.params import ENV_NAME, TEST_NAME

env = gym.make(f"gym_pygame/{ENV_NAME}", render_mode="human")
model = PPO('MultiInputPolicy', env, learning_rate=1e-3, verbose=2)
model = model.load(f"./model/{ENV_NAME}-{TEST_NAME}")
# Evaluate the agent
# mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
# print(mean_reward, std_reward)
# Enjoy trained agent
obs, info = env.reset(option="demo")
for i in range(10000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    if done or truncated:
        obs, infos = env.reset(option="demo")
    env.render()
