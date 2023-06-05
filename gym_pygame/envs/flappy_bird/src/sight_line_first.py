import math
from abc import ABC

from gym_envs.flappy_bird.src.sight_line import SightLine


class SightLineFirst(SightLine, ABC):
    def vision(self, pipes):
        distances = []
        # We compute distances between the line and every pipe
        for pipe in pipes:
            distances.append(self.check_collision_pipe(pipe))
        distances.append(self.check_collision_ground())
        distances.append(self.check_collision_sky())
        # We keep the min
        if distances:
            self.distance = min(distances)

    def color(self):
        return "red"
