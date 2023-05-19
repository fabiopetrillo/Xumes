from abc import ABC

import numpy as np

from envs.hide_and_seek.src.entity import get_tile_from_position
from envs.hide_and_seek.src.sight_line import SightLine


class SightLineFirst(SightLine, ABC):

    def vision(self):
        # We compute distances between the line and every pipe
        distance, type_wall = self.check_collision_wall()

        # We keep the min
        if distance < self.distance and (distance < 2000 or self.last_distance > 2000):
            self.distance = distance
            self.last_distance = distance
            self.type = type_wall
            self.last_type = type_wall
        else:
            self.distance = self.last_distance
            self.type = self.last_type

    def color(self):
        return "red"
