import math

import numpy as np
import pygame

from envs.hide_and_seek.params import BOARD_SIZE, NB_RAYS
from envs.hide_and_seek.src.entity import get_tile_from_position
from envs.hide_and_seek.src.ground import Ground
from envs.hide_and_seek.src.sight_line_first import SightLineFirst
from envs.hide_and_seek.src.wall import Wall


class Lidar:

    def __init__(self, board, player):
        self.board = board
        self.player = player
        theta = math.pi / 4
        self.tiles_enemies_map = {}
        self.sight_lines = []
        nb_rays = NB_RAYS
        for i in range(nb_rays):
            self.sight_lines.append(SightLineFirst(self.board, self.player, theta, 0, 0, self.tiles_enemies_map))
            theta += 2 * math.pi / nb_rays

    def draw(self, canvas):
        for line in self.sight_lines:
            line.draw(canvas)

    def vision(self):
        self.tiles_enemies_map.clear()
        for enemy in self.board.enemies:
            enemy_top_left_x, enemy_top_left_y = enemy.x, enemy.y
            enemy_top_right_x, enemy_top_right_y = enemy_top_left_x + enemy.size_x, enemy_top_left_y
            enemy_bottom_right_x, enemy_bottom_right_y = enemy_top_left_x + enemy.size_x, enemy_top_left_y + enemy.size_y
            enemy_bottom_left_x, enemy_bottom_left_y = enemy_top_left_x, enemy_top_left_y + enemy.size_y
            enemy_corners = [(enemy_top_left_x, enemy_top_left_y), (enemy_top_right_x, enemy_top_right_y), (enemy_bottom_right_x, enemy_bottom_right_y), (enemy_bottom_left_x, enemy_bottom_left_y)]

            for (x, y) in enemy_corners:
                enemy_x, enemy_y = get_tile_from_position(x, y)
                if self.board.board[enemy_x][enemy_y] in self.tiles_enemies_map.keys():
                    self.tiles_enemies_map[self.board.board[enemy_x][enemy_y]].append(enemy)
                else:
                    self.tiles_enemies_map[self.board.board[enemy_x][enemy_y]] = [enemy]

        for line in self.sight_lines:
            line.reset()
            line.vision()


    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        idx = 0
        player_center_x, player_center_y = self.player.center()
        for line in self.sight_lines:
            idx += 1
            text_surface = my_font.render(f'line({idx}): { 0 if line.type == Wall else 1 if line.type == Ground else 2}',
                                          False, (0, 0, 0))
            canvas.blit(text_surface, (0, 40 + 20 * idx))

    def reset(self):
        for line in self.sight_lines:
            line.reset()
