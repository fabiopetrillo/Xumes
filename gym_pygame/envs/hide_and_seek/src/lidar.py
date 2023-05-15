import math

import pygame

from envs.hide_and_seek.src.sight_line_first import SightLineFirst


class Lidar:

    def __init__(self, board, player):
        self.board = board
        self.player = player
        theta = 0
        self.sight_lines = []
        nb_lazer = 5
        for i in range(nb_lazer):
            self.sight_lines.append(SightLineFirst(self.player, theta))
            if theta != -theta:
                self.sight_lines.append(SightLineFirst(self.player, theta))
            theta += 2 * math.pi / nb_lazer

    def draw(self, canvas):
        for line in self.sight_lines:
            line.draw(canvas)

    def vision(self):
        for line in self.sight_lines:
            line.reset()
        for wall in self.board.wall_graph.keys():
            for line in self.sight_lines:
                line.vision(wall)

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
