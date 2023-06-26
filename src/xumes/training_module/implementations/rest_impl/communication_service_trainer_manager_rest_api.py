from flask import Flask, request

from xumes.training_module.i_communication_service_trainer_manager import ICommunicationServiceTrainerManager


class CommunicationServiceTrainerManagerRestApi(ICommunicationServiceTrainerManager):
    """
    The `CommunicationServiceTrainerManagerRestApi` class implements the `ICommunicationServiceTrainerManager` interface.
    """

    def __init__(self):
        self.app = Flask(__name__)

    def connect_trainer(self, trainer_manager) -> None:
        @self.app.route("/connect", methods=['POST'])
        def connect():
            feature, scenario, mode = request.json['feature'], request.json['scenario'], request.json['mode']
            trainer_manager.connect_trainer(feature, scenario, mode)
            return {"port": trainer_manager.get_port(feature, scenario)}

    def disconnect_trainer(self, trainer_manager) -> None:
        @self.app.route("/disconnect", methods=['POST'])
        def disconnect():
            feature, scenario = request.json['feature'], request.json['scenario']
            trainer_manager.disconnect_trainer(feature, scenario)
            return "Trainer disconnected!"

    def run(self, trainer_manager) -> None:
        self.connect_trainer(trainer_manager)
        self.disconnect_trainer(trainer_manager)
        self.app.run()
