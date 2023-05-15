import gym_pygame
import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

from envs.hide_and_seek.params import ENV_NAME, TEST_NAME


env = gym.make(f"gym_pygame/{ENV_NAME}")

# Instantiate the agent
model = PPO('MultiInputPolicy', env, learning_rate=1e-3, verbose=1)
# Train the agent
model.learn(total_timesteps=int(2e4))
# Save the agent
model.save(f"./model/{ENV_NAME}-{TEST_NAME}")

env.close()
env = gym.make(f"gym_pygame/{ENV_NAME}", render_mode="human")

# Evaluate the agent
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

# Enjoy trained agent
for i in range(100):
    obs, infos = env.reset(option="demo")
    dones = False
    truncated = False
    while not (dones or truncated):
        action, _states = model.predict(obs)
        obs, rewards, dones, truncated, info = env.step(action)
        env.render()
