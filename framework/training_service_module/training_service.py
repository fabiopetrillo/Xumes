from framework.training_service_module.i_action_converter import IActionConverter
from framework.training_service_module.i_communication_service import ICommunicationService
from framework.training_service_module.entity_manager import EntityManager
from framework.training_service_module.i_observation_maker import IObservationMaker
from framework.training_service_module.trainer import _Trainer


class TrainingService:

    def __init__(self,
                 entity_manager: EntityManager,
                 trainer: _Trainer,
                 communication_service: ICommunicationService,
                 action_converter: IActionConverter,
                 observation_maker: IObservationMaker
                 ):
        self._entity_manager = entity_manager
        self._trainer = trainer
        self._communication_service = communication_service
        self._action_converter = action_converter
        self._observation_maker = observation_maker

        self._trainer.set_training_service(self)

    def train(self):
        self._trainer.train()

    def save(self, path: str):
        self._trainer.save(path)

    def load(self, path: str):
        self._trainer.load(path)

    def play(self, timesteps: int):
        self._trainer.play(timesteps)

    def push_action(self, actions):
        self._communication_service.push_actions(
            actions=self._action_converter.convert(actions)
        )

    def get_obs(self):
        for state in self._communication_service.get_states():
            self._entity_manager.convert(state)
        return self._observation_maker.get_obs(entity_manager=self._entity_manager)

    def random_reset(self):
        self._communication_service.push_event("random_reset")

    def reset(self):
        self._communication_service.push_event("reset")

    def reward(self):
        return self._observation_maker.get_reward(self._entity_manager)

    def terminated(self):
        return self._observation_maker.get_terminated(self._entity_manager)
