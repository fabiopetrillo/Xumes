import sys

from gymnasium.vector.utils import spaces
import stable_baselines3

from framework.training_service_module.i_game_element_state_builder import JsonGameElementStateBuilder
from framework.training_service_module.implementations.gym_impl.stable_baselines_trainer import StableBaselinesTrainer
from framework.training_service_module.implementations.mq_impl.communication_service_mq import CommunicationServiceMq
from framework.training_service_module.training_service import TrainingService
from games_examples.snake.test_training_service.entities.snake_entity_manager import SnakeEntityManager
from games_examples.snake.test_training_service.game_obs_maker import SnakeObservationMaker
from games_examples.snake.test_training_service.snake_action_converter import SnakeActionConverter

if __name__ == "__main__":
    training_service = TrainingService(
        entity_manager=SnakeEntityManager(
            JsonGameElementStateBuilder()
        ),
        trainer=StableBaselinesTrainer(
            observation_space=spaces.Dict({
                "fruit_above_snake": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "fruit_right_snake": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "fruit_below_snake": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "fruit_left_snake": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "obstacle_above": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "obstacle_right": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "obstacle_bellow": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "obstacle_left": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "direction_up": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "direction_right": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "direction_down": spaces.Box(0, 1, shape=(1, ), dtype=int),
                "direction_left": spaces.Box(0, 1, shape=(1, ), dtype=int),
            }),
            action_space=spaces.Discrete(5),
            max_episode_length=500,
            total_timesteps=int(2e5),
            algorithm_type="MultiInputPolicy",
            algorithm=stable_baselines3.PPO
        ),
        communication_service=CommunicationServiceMq(),
        action_converter=SnakeActionConverter(),
        observation_maker=SnakeObservationMaker()
    )

    if len(sys.argv) == 2:
        if sys.argv[1] == "-train":
            training_service.train()
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model")
            training_service.play(100000)
