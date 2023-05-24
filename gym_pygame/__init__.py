from gymnasium.envs.registration import register

register(
    id="gym_pygame/RLFlappy-flappy_bird",
    entry_point="gym_pygame.envs.flappy_bird:FlappyEnv",
    max_episode_steps=2000,
)


register(
    id="gym_pygame/HNS-v0",
    entry_point="gym_pygame.envs.hide_and_seek:HideAndSeekEnv",
    max_episode_steps=1000,
)
