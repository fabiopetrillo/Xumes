import math
import numpy as np
from gym_envs.flappy_bird.src.sight_line import SightLine


class SightLineSecond(SightLine):
    def vision(self, pipes):
        distances = []
        # We compute distances between the line and every pipe
        for pipe in pipes:
            distances.append(self.check_collision_pipe(pipe))
        distances.append(self.check_collision_ground())
        # We keep the second min
        if distances:
            distances.remove(min(distances))
            if distances:
                self.distance = min(distances)

    def color(self):
        return "blue"
