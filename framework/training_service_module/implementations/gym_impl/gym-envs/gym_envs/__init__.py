from gymnasium.envs.registration import register

register(
    id="gym_env-v0",
    entry_point="gym_envs.gym_adapter_env.gym_adapter:GymAdapter",
)
