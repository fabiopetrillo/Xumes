import numpy as np

from framework.training_service_module.entity_manager import EntityManager
from framework.training_service_module.i_observation_maker import IObservationMaker
from games_examples.snake.play import cell_number


class SnakeObservationMaker(IObservationMaker):

    def __init__(self):
        self.distance = float('inf')

    def get_obs(self, entity_manager: EntityManager):
        snake = entity_manager.get("snake")
        snake_head = snake.body[0]
        fruit = entity_manager.get("fruit")

        return {
            "fruit_above_snake": np.array([1 if snake_head[1] > fruit.y else 0]),
            "fruit_right_snake": np.array([1 if snake_head[0] < fruit.x else 0]),
            "fruit_below_snake": np.array([1 if snake_head[1] < fruit.y else 0]),
            "fruit_left_snake": np.array([1 if snake_head[0] > fruit.x else 0]),
            "obstacle_above": np.array(
                [1 if snake_head[1] - 1 == 0 or (snake_head[0], snake_head[1] - 1) in snake.body else 0]),
            "obstacle_right": np.array(
                [1 if snake_head[0] + 1 == cell_number or (snake_head[0] + 1, snake_head[1]) in snake.body else 0]),
            "obstacle_bellow": np.array(
                [1 if snake_head[1] + 1 == cell_number or (snake_head[0], snake_head[1] + 1) in snake.body else 0]),
            "obstacle_left": np.array(
                [1 if snake_head[0] - 1 == 0 or (snake_head[0] - 1, snake_head[1]) in snake.body else 0]),
            "direction_up": np.array([1 if snake.direction == (0, -1) else 0]),
            "direction_right": np.array([1 if snake.direction == (1, 0) else 0]),
            "direction_down": np.array([1 if snake.direction == (0, 1) else 0]),
            "direction_left": np.array([1 if snake.direction == (-1, 0) else 0]),
        }

    def get_reward(self, entity_manager: EntityManager) -> float:
        snake = entity_manager.get("snake")
        fruit = entity_manager.get("fruit")

        head_x, head_y = snake.body[0][0], snake.body[0][1]
        distance = np.abs(fruit.x - head_x) + np.abs(fruit.y - head_y)

        if distance < self.distance:
            close_reward = 1
        elif distance > self.distance:
            close_reward = -1
        else:
            close_reward = 0

        if entity_manager.game_state == "fruit_ate":
            return 10
        elif entity_manager.game_state == "lose":
            return -100
        else:
            return close_reward

    def get_terminated(self, entity_manager) -> bool:
        return entity_manager.game_state == "lose" or entity_manager.game_state == "reset" or entity_manager.game_state == "random_reset"
