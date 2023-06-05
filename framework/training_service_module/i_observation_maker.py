from framework.training_service_module.entity_manager import EntityManager


class IObservationMaker:

    def get_obs(self, entity_manager: EntityManager):
        pass

    def get_reward(self, entity_manager: EntityManager) -> float:
        pass

    def get_terminated(self, entity_manager) -> bool:
        pass
