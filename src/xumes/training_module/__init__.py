from xumes.training_module.trainer_manager import observation, reward, action, config, terminated, StableBaselinesTrainerManager, VecStableBaselinesTrainerManager
from gymnasium.envs.registration import register

register(
    id="xumes-v0",
    entry_point="xumes.training_module.implementations.gym_impl.gym_envs.gym_env.gym_adapter_env.gym_adapter:GymAdapter",
)
