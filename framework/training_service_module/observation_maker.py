from framework.training_service_module.entity_manager import EntityManager


class IObservationMaker:

    def get_obs(self, entity_manager: EntityManager):
        pass
