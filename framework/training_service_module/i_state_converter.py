from typing import TypeVar

from framework.training_service_module.entity_manager import EntityManager

OBST = TypeVar("OBST")


class IStateConverter:

    def convert_obs(self, entity_manager: EntityManager) -> OBST:
        pass

    def convert_reward(self, entity_manager: EntityManager) -> float:
        pass

    def convert_terminated(self, entity_manager: EntityManager) -> bool:
        pass
