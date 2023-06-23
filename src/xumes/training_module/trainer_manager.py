import importlib
import inspect
import os
import sys
import threading
from abc import abstractmethod
from typing import List

from xumes.training_module import StableBaselinesTrainer, AutoEntityManager, JsonGameElementStateConverter, \
    CommunicationServiceTrainingMq
from xumes.training_module.implementations.gym_impl.stable_baselines_trainer import OBST
from xumes.training_module.implementations.rest_impl.communication_service_trainer_manager_rest_api import \
    CommunicationServiceTrainerManagerRestApi
from xumes.training_module.training_service import TrainingService

TRAIN_MODE = "train"
TEST_MODE = "test"


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def create_registry():
    registry = {}

    def registrar(func):
        file_path = inspect.getsourcefile(func)
        file_name = os.path.basename(file_path[:-3])
        registry[file_name] = func
        return func

    registrar.all = registry
    return registrar


def make_observation():
    return create_registry()


def make_action():
    return create_registry()


def make_reward():
    return create_registry()


def make_terminated():
    return create_registry()


def make_config():
    return create_registry()


class TrainerManager:
    observation = make_observation()
    action = make_action()
    reward = make_reward()
    terminated = make_terminated()
    config = make_config()

    def __init__(self):
        for file in os.listdir("./trainers"):
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join("./trainers", file)
                module = compile(open(module_path).read(), module_path, 'exec')
                exec(module, globals(), locals())
                module_dep = importlib.import_module(f"trainers.{module_name}")

        self._trainer_threads = {}
        self._trainer_objects = {}

        self._communication_service = CommunicationServiceTrainerManagerRestApi()

    def run(self):
        self._communication_service.run(self)

    def connect_trainer(self, feature: str, scenario: str, port: int, mode: str) -> None:
        """
        Connects a trainer to the training module.

        :param feature:
        :param scenario:
        :param port:
        :param mode:
        :return:
        """
        trainer = self.create_trainer(feature, scenario, port, mode)

        self._trainer_objects[feature + scenario] = trainer

        if mode == TRAIN_MODE:
            thread = thread_with_trace(target=trainer.train,
                                       args=("./models/" + feature + "/" + scenario + "/",))
            self._trainer_threads[feature + scenario] = thread
            thread.start()
        elif mode == TEST_MODE:
            thread = thread_with_trace(target=trainer.load_and_play,
                                       args=(None, "./models/" + feature + "/" + scenario + "/best_model.zip",))
            self._trainer_threads[feature + scenario] = thread
            thread.start()

    def disconnect_trainer(self, feature: str, scenario: str) -> None:
        if feature + scenario in self._trainer_threads and feature + scenario in self._trainer_objects:
            self._trainer_objects[feature + scenario].close_communication()
            self._trainer_threads[feature + scenario].kill()
            self._trainer_threads[feature + scenario].join()
            del self._trainer_threads[feature + scenario]
            del self._trainer_objects[feature + scenario]

    @abstractmethod
    def create_trainer(self, feature: str, scenario: str, port: int, mode: str) -> TrainingService:
        raise NotImplementedError


observation = TrainerManager.observation
action = TrainerManager.action
reward = TrainerManager.reward
terminated = TrainerManager.terminated
config = TrainerManager.config


class StableBaselinesTrainerManager(TrainerManager):
    def create_trainer(self, feature: str, scenario: str, port: int, mode: str) -> TrainingService:
        class Trainer(StableBaselinesTrainer):
            def convert_obs(self) -> OBST:
                return observation.all[feature](self)

            def convert_reward(self) -> float:
                return reward.all[feature](self)

            def convert_terminated(self) -> bool:
                return terminated.all[feature](self)

            def convert_actions(self, raws_actions) -> List[str]:
                return action.all[feature](self, raws_actions)

        try:
            trainer = Trainer(entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
                              communication_service=CommunicationServiceTrainingMq(port=port))

            configuration = config.all[feature](trainer)
            trainer.observation_space = configuration["observation_space"]
            trainer.action_space = configuration["action_space"]
            trainer.max_episode_length = configuration["max_episode_length"]
            trainer.total_timesteps = configuration["total_timesteps"]
            trainer.algorithm_type = configuration["algorithm_type"]
            trainer.algorithm = configuration["algorithm"]
            trainer.random_reset_rate = configuration["random_reset_rate"]

            trainer.make()
        except Exception as e:
            raise Exception(f"Error while creating trainer: {e}")

        return trainer
