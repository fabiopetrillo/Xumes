import math

import pygame

from src.sight_line import SightLine


class Lidar:

    def __init__(self, pipe_generator, player, screen):
        self.pipe_generator = pipe_generator
        self.player = player
        self.sight_lines = [
            SightLine(self.player, math.pi / 4, screen),
            SightLine(self.player, - math.pi / 4, screen),
            SightLine(self.player, math.pi / 6, screen),
            SightLine(self.player, -math.pi / 6, screen),
            SightLine(self.player, 0, screen),
        ]
        self.screen = screen

    def draw(self):
        for line in self.sight_lines:
            line.draw()

    def vision(self):
        for line in self.sight_lines:
            distances = []
            # We compute distances between the line and every pipe
            for pipe in self.pipe_generator.pipes:
                distances.append(line.check_collision_pipe(pipe))

            # We keep the min
            if distances:
                line.distance = min(distances)

    def logs(self):
        my_font = pygame.font.SysFont('Arial', 14)
        idx = 0
        for line in self.sight_lines:
            idx += 1
            text_surface = my_font.render(f'line({idx}): {int(line.distance)}',
                                          False, (0, 0, 0))
            self.screen.blit(text_surface, (0, 40 + 20 * idx))
