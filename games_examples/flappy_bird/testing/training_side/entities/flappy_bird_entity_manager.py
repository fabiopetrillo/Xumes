from games_examples.flappy_bird.testing.training_side.entities.bird_entity import BirdEntity
from games_examples.flappy_bird.testing.training_side.entities.pipes_entity import PipesEntity
from xumes.training_module import EntityManager


class FlappyBirdEntityManager(EntityManager):

    def build_entity(self, game_element_state):
        if game_element_state.type == "Player":
            return BirdEntity.build(game_element_state.state)
        if game_element_state.type == "PipeGenerator":
            return PipesEntity.build(game_element_state.state)
