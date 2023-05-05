from gymnasium.envs.registration import register

register(
    id="gym_pygame/RLFlappy-v0",
    entry_point="gym_pygame.envs:FlappyEnv",
    max_episode_steps=300,
)
