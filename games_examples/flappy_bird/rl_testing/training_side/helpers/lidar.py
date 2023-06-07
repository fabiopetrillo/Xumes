import math

from games_examples.flappy_bird.rl_testing.training_side.entities.bird_entity import BirdEntity
from games_examples.flappy_bird.rl_testing.training_side.entities.pipes_entity import PipesEntity
from games_examples.flappy_bird.rl_testing.training_side.helpers.sight_line import SightLineFirst


class Lidar:

    def __init__(self, pipes: PipesEntity, bird: BirdEntity):
        self.pipes = pipes
        self.bird = bird
        self.sight_lines = [
            SightLineFirst(self.bird, math.pi / 6),
            SightLineFirst(self.bird, - math.pi / 6),
            SightLineFirst(self.bird, math.pi / 4),
            SightLineFirst(self.bird, - math.pi / 4),
            SightLineFirst(self.bird, math.pi / 12),
            SightLineFirst(self.bird, -math.pi / 12),
            SightLineFirst(self.bird, 0),
        ]

    def vision(self):
        for line in self.sight_lines:
            line.vision(self.pipes)

    def reset(self):
        for line in self.sight_lines:
            line.reset()
