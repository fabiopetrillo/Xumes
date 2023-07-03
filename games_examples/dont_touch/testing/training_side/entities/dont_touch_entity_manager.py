from xumes.training_module import EntityManager

from games_examples.dont_touch.testing.training_side.entities.hand_entity import HandEntity
from games_examples.dont_touch.testing.training_side.entities.player_entity import PlayerEntity


class BatKillerEntityManager(EntityManager):

    def build_entity(self, game_element_state):
        if game_element_state.type == "Player":
            return PlayerEntity.build(game_element_state.state)
        if game_element_state.type == "Hand":
            return HandEntity.build(game_element_state.state)
