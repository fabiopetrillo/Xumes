from framework.training_service_module.entity_manager import EntityManager
from framework.training_service_module.game_element_state import GameElementState
from framework.training_service_module.i_state_entity import IStateEntity
from games_examples.flappy_bird.testing.training_side.entities.bird_entity import BirdEntity
from games_examples.flappy_bird.testing.training_side.entities.pipes_entity import PipesEntity


class FlappyBirdEntityManager(EntityManager):

    def build_entity(self, game_element_state: GameElementState) -> IStateEntity:
        if game_element_state.type == "Player":
            return BirdEntity.build(game_element_state.state)
        if game_element_state.type == "PipeGenerator":
            return PipesEntity.build(game_element_state.state)
