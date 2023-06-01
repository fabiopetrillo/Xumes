import requests
from gym.vector.utils import spaces
from stable_baselines3 import PPO

from framework.training_service_module.game_element_state_builder import JsonGameElementStateBuilder
from framework.training_service_module.gym_helpers.stable_baselines_trainer import StableBaselinesTrainer
from games_examples.snake.test_training_service.entities.snake_entity_factory import SnakeEntityManager

r = requests.get("http://localhost:5000/")

d = r.json()

entity_manager = SnakeEntityManager(
    game_element_state_builder=JsonGameElementStateBuilder()
)


for state_wrapper in d.items():
    entity_manager.convert(state_wrapper)


trainer = StableBaselinesTrainer(
    observation_space={
        "snake": spaces.Box(0, float('inf'), shape=(20, 2), dtype=float),
        "fruit": spaces.Box(0, float('inf'), shape=(2,), dtype=float),
    },
    action_space=spaces.Discrete(5),
    max_episode_length=100,
    total_timesteps=20000,
    algorithm_type="MultiInputPolicy",
    algorithm=PPO
)


