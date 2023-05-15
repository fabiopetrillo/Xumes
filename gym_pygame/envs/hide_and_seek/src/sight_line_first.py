from abc import ABC

from envs.hide_and_seek.src.sight_line import SightLine


class SightLineFirst(SightLine, ABC):
    def vision(self, wall):
        # We compute distances between the line and every pipe
        distance = self.check_collision_wall(wall)

        # We keep the min
        if distance < self.distance:
            self.distance = distance

    def color(self):
        return "red"
