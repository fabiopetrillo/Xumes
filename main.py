import gymnasium as gym
import gym_pygame

env = gym.make('gym_pygame/RLFlappy-v0', render_mode="human")
observation, info = env.reset()

for _ in range(1000):

    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    print(action, info, observation, terminated)

    if terminated:  # TODO check truncated
        observation, info = env.reset()

env.close()
