from framework.training_service_module.entity_manager import EntityManager
from framework.training_service_module.observation_maker import IObservationMaker


class SnakeObservationMaker(IObservationMaker):

    def get_obs(self, entity_manager: EntityManager):
        return {
            "snake": entity_manager.get("snake").body,
            "fruit": [entity_manager.get("fruit").x, entity_manager.get("fruit").y],
        }
