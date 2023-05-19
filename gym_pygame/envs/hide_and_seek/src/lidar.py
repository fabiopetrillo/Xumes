import math

import pygame

from envs.hide_and_seek.src.sight_line_first import SightLineFirst
from envs.hide_and_seek.src.wall import Wall


class Lidar:

    def __init__(self, board, player):
        self.board = board
        self.player = player
        theta = math.pi / 4

        half_player_x, half_player_y = self.player.size_x / 2, self.player.size_y / 2
        self.sight_lines = [
            SightLineFirst(self.board, self.player, 0, half_player_x, 0),
            SightLineFirst(self.board, self.player, math.pi / 4, half_player_x, half_player_y),
            SightLineFirst(self.board, self.player, math.pi / 2, 0, half_player_y),
            SightLineFirst(self.board, self.player, 3 * math.pi / 4, -half_player_x, half_player_y),
            SightLineFirst(self.board, self.player, math.pi, -half_player_x, 0),
            SightLineFirst(self.board, self.player, -math.pi / 4, half_player_x, -half_player_y),
            SightLineFirst(self.board, self.player, -math.pi / 2, 0, -half_player_y),
            SightLineFirst(self.board, self.player, -3 * math.pi / 4, -half_player_x, -half_player_y),
        ]
        # nb_lazer = 8
        # for i in range(nb_lazer):
        #     self.sight_lines.append(SightLineFirst(self.board, self.player, theta))
        #     theta += 2 * math.pi / nb_lazer

    def draw(self, canvas):
        for line in self.sight_lines:
            line.draw(canvas)

    def vision(self):
        for line in self.sight_lines:
            line.reset()
            line.vision()


    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        idx = 0
        player_center_x, player_center_y = self.player.center()
        for line in self.sight_lines:
            idx += 1
            text_surface = my_font.render(f'line({idx}): {int(line.distance)} {int(line.end_y - player_center_y)} {int(line.end_x - player_center_x)} {0 if line.type == Wall else 1}',
                                          False, (0, 0, 0))
            canvas.blit(text_surface, (0, 40 + 20 * idx))

    def reset(self):
        for line in self.sight_lines:
            line.reset()
