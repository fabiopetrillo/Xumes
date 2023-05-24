import math

import pygame

from envs.flappy_bird.src.sight_line_first import SightLineFirst
from envs.flappy_bird.src.sight_line_snd import SightLineSecond


class Lidar:

    def __init__(self, pipe_generator, player):
        self.pipe_generator = pipe_generator
        self.player = player
        self.sight_lines = [
            SightLineFirst(self.player, math.pi / 6),
            SightLineFirst(self.player, - math.pi / 6),
            SightLineFirst(self.player, math.pi / 4),
            SightLineFirst(self.player, - math.pi / 4),
            SightLineFirst(self.player, math.pi / 12),
            SightLineFirst(self.player, -math.pi / 12),
            SightLineFirst(self.player, 0),
        ]

    def draw(self, canvas):
        for line in self.sight_lines:
            line.draw(canvas)

    def vision(self):
        for line in self.sight_lines:
            line.vision(self.pipe_generator.pipes)

    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        idx = 0
        for line in self.sight_lines:
            idx += 1
            text_surface = my_font.render(f'line({idx}): {int(line.distance)}',
                                          False, (0, 0, 0))
            canvas.blit(text_surface, (0, 40 + 20 * idx))

    def reset(self):
        for line in self.sight_lines:
            line.reset()