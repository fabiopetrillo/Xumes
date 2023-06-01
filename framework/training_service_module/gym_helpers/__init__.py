from gymnasium.envs.registration import register

register(
    id="gym_env",
    entry_point="gym_helpers.envs.gym_adapter:GymAdapter",
)

