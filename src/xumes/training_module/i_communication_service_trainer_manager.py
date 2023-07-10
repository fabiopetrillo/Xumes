from typing import List, TypeVar

SW = TypeVar("SW")


class ICommunicationServiceTrainerManager:
    """
    The `ICommunicationServiceTrainerManager` interface defines the methods for communicate from the game test manager to the trainer manager.

    Methods:
        connect_trainer: Connect the trainer manager to the game test manager.
        disconnect_trainer: Disconnect the trainer manager from the game test manager.
    """
    def connect_trainer(self, trainer_manager, tasks, task_condition) -> None:
        raise NotImplementedError

    def disconnect_trainer(self, trainer_manager, tasks, task_condition) -> None:
        raise NotImplementedError

    def start_training(self, trainer_manager, tasks, task_condition) -> None:
        raise NotImplementedError

    def reset(self, trainer_manager, tasks, task_condition) -> None:
        raise NotImplementedError

    def run(self, trainer_manager, tasks, task_condition, port) -> None:
        raise NotImplementedError
