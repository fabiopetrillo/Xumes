import importlib.util
import importlib.util
import logging
import os
import threading
from abc import abstractmethod
from multiprocessing import Process
from queue import Queue, Empty
from typing import List

from xumes.core.registry import create_registry
from xumes.training_module import StableBaselinesTrainer, AutoEntityManager, JsonGameElementStateConverter, \
    CommunicationServiceTrainingMq
from xumes.training_module.i_communication_service_trainer_manager import ICommunicationServiceTrainerManager
from xumes.training_module.i_trainer import ITrainer
from xumes.training_module.implementations.gym_impl.stable_baselines_trainer import OBST
from xumes.training_module.implementations.gym_impl.vec_stable_baselines_trainer import VecStableBaselinesTrainer

TRAIN_MODE = "train"
TEST_MODE = "test"
FEATURE_MODE = "feature"
SCENARIO_MODE = "scenario"


class TrainerManager:
    """
    Base class for trainer managers.

    Args:
        communication_service (ICommunicationServiceTrainerManager): The communication service for the trainer manager.
        mode (str, optional): The mode of the trainer manager. Defaults to TEST_MODE.
        port (int, optional): The port number for the communication service. Defaults to 5000.
    """
    def __init__(self, communication_service: ICommunicationServiceTrainerManager, mode: str = TEST_MODE,
                 port: int = 5000):
        # Load all trainers
        for file in os.listdir("./trainers"):
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join("./trainers", file)
                module = compile(open(module_path).read(), module_path, 'exec')
                exec(module, globals(), locals())
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

        self._trainer_processes = {}
        self._mode = mode
        self._communication_service = communication_service
        self._tasks = Queue()
        self._task_condition = threading.Condition()
        self._port = port

    def run(self):
        # Create a thread to run the communication service
        threading.Thread(target=self._communication_service.run,
                         args=(self, self._tasks, self._task_condition, self._port)).start()

        start_training = False

        # We will run the communication service until we receive a "start_training" task
        while True:
            with self._task_condition:
                self._task_condition.wait()
            while not self._tasks.empty():
                try:
                    task = self._tasks.get(block=False)
                    func = task[0]
                    if func == "start_training":
                        start_training = True
                        break
                    else:
                        args = task[1:]
                        func(*args)
                except Empty:
                    break
            if start_training:
                break

    def connect_trainer(self, feature: str, scenario: str, port: int) -> None:
        # Create a new process to train or use an agent
        name = self._trainer_name(feature, scenario)

        if self._mode == TRAIN_MODE:
            process = Process(target=self.create_and_train, args=(feature, scenario, port,))
            self._trainer_processes[name] = process
            process.start()
        elif self._mode == TEST_MODE:
            process = Process(target=self.create_and_play, args=(feature, scenario, port,))
            self._trainer_processes[name] = process
            process.start()

    def disconnect_trainer(self, feature: str, scenario: str) -> None:
        # Terminate the process
        name = self._trainer_name(feature, scenario)
        if name in self._trainer_processes:
            self._trainer_processes[name].terminate()
            self._trainer_processes[name].join()
            del self._trainer_processes[name]

    def create_and_train(self, feature: str, scenario: str, port: int):
        # Create a new trainer and train it
        trainer = self.create_trainer(feature, scenario, port)
        trainer.train(self._model_path(feature, scenario))

    def create_and_play(self, feature: str, scenario: str, port: int):
        # Create a new trainer and play it
        trainer = self.create_trainer(feature, scenario, port)
        trainer.load(self._model_path(feature, scenario) + "/best_model")
        trainer.play(timesteps=None)

    @abstractmethod
    def create_trainer(self, feature: str, scenario: str, port: int) -> ITrainer:
        # Abstract method to create a trainer for a specific feature and scenario
        # This method should be implemented by the concrete trainer manager
        raise NotImplementedError

    @abstractmethod
    def _trainer_name(self, feature, scenario) -> str:
        # Abstract method to create a trainer name for a specific feature and scenario
        # This method should be implemented by the concrete trainer manager
        raise NotImplementedError

    @abstractmethod
    def _model_path(self, feature, scenario) -> str:
        # Abstract method to create a model path for a specific feature and scenario
        # This method should be implemented by the concrete trainer manager
        raise NotImplementedError


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


class StableBaselinesTrainerManager(TrainerManager):
    """
    Concrete trainer manager for stable baselines trainers
    Use to train each agent on a different model
    """
    observation = make_observation()
    action = make_action()
    reward = make_reward()
    terminated = make_terminated()
    config = make_config()

    def create_trainer(self, feature: str, scenario: str, port: int) -> ITrainer:
        # We use the decorators to implement the trainer's methods

        class ConcreteTrainer(StableBaselinesTrainer):
            def convert_obs(self) -> OBST:
                return observation.all[feature](self)

            def convert_reward(self) -> float:
                return reward.all[feature](self)

            def convert_terminated(self) -> bool:
                return terminated.all[feature](self)

            def convert_actions(self, raws_actions) -> List[str]:
                return action.all[feature](self, raws_actions)

        try:
            trainer = ConcreteTrainer(entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
                                      communication_service=CommunicationServiceTrainingMq(port=port))

            config.all[feature](trainer)
            trainer.make()
        except Exception as e:
            raise Exception(f"Error while creating trainer: {e}")

        return trainer

    def _trainer_name(self, feature, scenario) -> str:
        return feature + "_" + scenario

    def _model_path(self, feature, scenario) -> str:
        return "./models/" + feature + "/" + scenario


observation = StableBaselinesTrainerManager.observation
action = StableBaselinesTrainerManager.action
reward = StableBaselinesTrainerManager.reward
terminated = StableBaselinesTrainerManager.terminated
config = StableBaselinesTrainerManager.config


class VecStableBaselinesTrainerManager(StableBaselinesTrainerManager):
    """
    Concrete trainer manager for stable baselines trainers
    Use to train all agents on the same model
    """
    def __init__(self, communication_service: ICommunicationServiceTrainerManager, port: int):
        super().__init__(communication_service, port=port)

        # Create a vectorized trainer
        # This trainer will train all agents on the same model
        self.vec_trainer = VecStableBaselinesTrainer()
        self._trained_feature = None

    def connect_trainer(self, feature: str, scenario: str, port: int) -> None:
        # Add a new training service to the vectorized trainer
        if self._trained_feature is None:
            self._trained_feature = feature
        self.vec_trainer.add_training_service(self.create_trainer(feature, scenario, port))

    def train(self):
        self.vec_trainer.make()
        logging.info("Training model")
        self.vec_trainer.train()
        logging.info("Saving model")
        self.vec_trainer.save(self._model_path(self._trained_feature, "") + "/best_model")

    def play(self, timesteps: int = None):
        self.vec_trainer.make()
        logging.info("Loading model")
        self.vec_trainer.load(self._model_path(self._trained_feature, "") + "/best_model")
        logging.info("Playing model")
        self.vec_trainer.play(timesteps)

    def _trainer_name(self, feature, scenario) -> str:
        return feature

    def _model_path(self, feature, scenario) -> str:
        return "./models/" + feature
