from flask import Flask, request

from xumes.training_module.i_communication_service_trainer_manager import ICommunicationServiceTrainerManager


class CommunicationServiceTrainerManagerRestApi(ICommunicationServiceTrainerManager):
    """
    The `CommunicationServiceTrainerManagerRestApi` class implements the `ICommunicationServiceTrainerManager` interface.
    """

    def __init__(self):
        self.app = Flask(__name__)

    def connect_trainer(self, trainer_manager, tasks, task_condition) -> None:
        @self.app.route("/connect", methods=['POST'])
        def connect():
            feature, scenario, port = request.json['feature'], request.json['scenario'], request.json['port']
            tasks.put((trainer_manager.connect_trainer, feature, scenario, port))
            with task_condition:
                task_condition.notify_all()
            return "Trainer connected!"

    def disconnect_trainer(self, trainer_manager, tasks, task_condition) -> None:
        @self.app.route("/disconnect", methods=['POST'])
        def disconnect():
            feature, scenario = request.json['feature'], request.json['scenario']
            tasks.put((trainer_manager.disconnect_trainer, feature, scenario))
            with task_condition:
                task_condition.notify_all()
            return "Trainer disconnected!"

    def start_training(self, trainer_manager, tasks, task_condition) -> None:
        @self.app.route("/start", methods=['POST'])
        def start_training():
            tasks.put(("start_training",))
            with task_condition:
                task_condition.notify_all()
            return "Training started!"

    def ping(self):
        @self.app.route("/ping", methods=['GET'])
        def ping():
            return "pong"

    def run(self, trainer_manager, tasks, task_condition, port) -> None:
        self.connect_trainer(trainer_manager, tasks, task_condition)
        self.disconnect_trainer(trainer_manager, tasks, task_condition)
        self.start_training(trainer_manager, tasks, task_condition)
        self.ping()
        self.app.run(port=port)
