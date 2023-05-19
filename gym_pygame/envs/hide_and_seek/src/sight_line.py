import math
from abc import abstractmethod
from typing import Union

import numpy as np
import pygame

from envs.hide_and_seek.src.entity import get_tile_from_position
from envs.hide_and_seek.src.ground import Ground
from envs.hide_and_seek.src.wall import Wall


def line_rect_intersection(line_start, line_end, rect):
    # Find the four corners of the rectangle
    corners = [(rect.left, rect.top), (rect.right, rect.top),
               (rect.right, rect.bottom), (rect.left, rect.bottom)]

    intersections = []
    for i in range(4):
        # Find the intersection point of the line and the current edge of the rectangle
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        x3, y3 = line_start
        x4, y4 = line_end

        if x2 - x1 == 0:  # Edge is vertical
            x_intersect = x1
            m = (y4 - y3) / (x4 - x3)
            b = y3 - m * x3
            y_intersect = m * x_intersect + b
        elif y2 - y1 == 0:  # Edge is horizontal
            y_intersect = y1
            m = (y4 - y3) / (x4 - x3)
            b = y3 - m * x3
            if m != 0:
                x_intersect = (y_intersect - b) / m
            else:
                x_intersect = float('inf')
        else:
            m1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - m1 * x1
            m2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - m2 * x3
            x_intersect = (b2 - b1) / (m1 - m2)
            y_intersect = m1 * x_intersect + b1

        # Check if the intersection point is on the line segment and within the rectangle
        if (min(x1, x2) <= x_intersect <= max(x1, x2) and
                min(y1, y2) <= y_intersect <= max(y1, y2) and
                min(x3, x4) <= x_intersect <= max(x3, x4) and
                min(y3, y4) <= y_intersect <= max(y3, y4)):
            intersections.append((x_intersect, y_intersect))

    return intersections


class SightLine:

    @abstractmethod
    def color(self):
        pass

    def __init__(self, board, player, angle, start_x, start_y):
        self.player = player
        self.board = board
        self.angle = angle
        self.max_length = 2000
        self.distance = 2000
        self.last_distance = 2000
        self.type = None
        self.last_type = None
        self.start_x = start_x
        self.start_y = start_y

    # Use to compute the new intersection
    def end_virtual_position(self):
        x, y = self.center()
        end_x = x + self.max_length * math.cos(self.angle)
        end_y = y + self.max_length * math.sin(self.angle)
        return end_x, end_y

    @property
    def end_x(self):
        return self.x + self.distance * math.cos(self.angle)

    @property
    def end_y(self):
        return self.y + self.distance * math.sin(self.angle)

    # Use to get the actual distance
    def end_position(self):
        x, y = self.center()
        end_x = x + self.distance * math.cos(self.angle)
        end_y = y + self.distance * math.sin(self.angle)
        return end_x, end_y

    def draw(self, canvas):
        pygame.draw.line(canvas, self.color(), self.center(), self.end_position())

    def check_collision_wall(self):

        walls = self._first_wall()
        distance, type_wall = 2000, None  # TODO remove magic number
        found_wall = False

        if walls:
            while not found_wall and walls:
                wall = walls.pop(0)
                type_wall = type(wall)
                intersections = line_rect_intersection(self.center(), self.end_virtual_position(), wall.rect)

                x_player, y_player = self.center()

                if intersections:
                    # For every intersections we keep the min distance
                    for (x, y) in intersections:
                        d = math.sqrt((x_player - x) ** 2 + (y_player - y) ** 2)
                        if d < distance:
                            distance = d
                    found_wall = True

        return distance, type_wall

    @property
    def x(self):
        return self.player.x + self.start_x

    @property
    def y(self):
        return self.player.y + self.start_y

    def center(self):
        player_x, player_y = self.player.center()
        return player_x + self.start_x, player_y + self.start_y

    def _first_wall(self):

        last_x, last_y = self.end_virtual_position()
        last_tile_x, last_tile_y = get_tile_from_position(last_x, last_y)
        player_tile_x, player_tile_y = get_tile_from_position(self.x, self.y)

        tiles = []
        # Distance in tile
        distance_last = np.sqrt(
            np.power(player_tile_x - last_tile_x, 2) + np.power(player_tile_y - last_tile_y, 2))

        # Here we gather all tile between the enemy and the player
        if distance_last > 1:
            # steps to take to reach the player
            diff_x, diff_y = (last_x - self.x) / (40 * distance_last), (
                    last_y - self.y) / (40 * distance_last)

            dist_x, dist_y = self.center()
            tile_x, tile_y = get_tile_from_position(dist_x, dist_y)

            # While the tile checked have not reached the player yet
            while abs(player_tile_x - last_tile_x) + abs(player_tile_y - last_tile_y) > abs(
                    tile_x - player_tile_x) + abs(tile_y - player_tile_y):
                # We walk of one step
                dist_x += diff_x
                dist_y += diff_y
                # Get the tile and add it to the to check list
                tile_x, tile_y = get_tile_from_position(dist_x, dist_y)

                if 0 <= tile_x <= self.board.size_x and 0 <= tile_y <= self.board.size_y:
                    tile = self.board.board[tile_x][tile_y]
                    if isinstance(tile, Wall):
                        tiles.append(tile)
                        return tiles
                    elif isinstance(tile, Ground):
                        if tile.has_coin:
                            tiles.append(tile)
                else:
                    return

    @abstractmethod
    def vision(self):
        pass

    def reset(self):
        self.max_length = 2000
        self.distance = 2000
        self.type = None
