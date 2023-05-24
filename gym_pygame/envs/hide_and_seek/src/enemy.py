import random
from abc import ABC
from typing import Optional, Dict, List

import numpy as np
import pygame

from envs.hide_and_seek.params import ENEMY_SIZE, ENEMY_VIEW_DIST, ENEMY_MEMORY, ENEMY_SPEED
from envs.hide_and_seek.src.entity import Entity, CONTROL_DOWN, CONTROL_TOP, CONTROL_LEFT, CONTROL_RIGHT, \
    get_tile_from_position
from envs.hide_and_seek.src.tile import Tile
from envs.hide_and_seek.src.utils.PriorityQueue import PriorityQueue
from envs.hide_and_seek.src.wall import Wall


def heuristic(a: Tile, b: Tile) -> float:
    # Heuristic use in the a star algorithm
    (x1, y1) = a.x, a.y
    (x2, y2) = b.x, b.y
    return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))


def reconstruct_path(came_from: Dict[Tile, Tile],
                     start: Tile, goal: Tile) -> List[Tile]:
    # Build a path after the a star algorithm
    current: Tile = goal
    path: List[Tile] = []
    if goal not in came_from:  # no path was found
        return []

    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def a_star_search(graph: dict, start: Tile, goal: Tile):
    # A star algorithm

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Tile, Optional[Tile]] = {}
    cost_so_far: Dict[Tile, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current: Tile = frontier.get()

        if current == goal:
            break

        for next in graph[current]:
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


class Enemy(Entity, ABC):

    def find_control(self, dt):

        # Compute the a star algorithm
        center_x, center_y = self.think_is_x, self.think_is_y
        goal_center_x, goal_center_y = self.board.player.center()
        start_ground_x, start_ground_y = get_tile_from_position(center_x, center_y)
        start = self.board.get_ground_from_position(start_ground_x, start_ground_y)
        goal_x, goal_y = get_tile_from_position(goal_center_x, goal_center_y)
        goal = self.board.get_ground_from_position(goal_x, goal_y)
        came_from, cost_so_far = a_star_search(self.board.reachable_ground_graph, start, goal)

        # Here we got the path
        self.path = reconstruct_path(came_from, start, goal)

        if not self.player_seen:
            # Use to not change of direction every time
            self.no_goal_dt -= dt
            if self.no_goal_dt <= 0:
                self.no_goal_dt = random.random() * 2
                self.base_control = np.random.choice([CONTROL_RIGHT, CONTROL_LEFT, CONTROL_TOP, CONTROL_DOWN])
        else:
            try:
                collision_x, collision_y = get_tile_from_position(center_x, center_y)
                start = self.board.get_ground_from_position(collision_x, collision_y)

                next_pos = self.path[0]
                start_x, start_y = start.x, start.y

                next_x, next_y = next_pos.x, next_pos.y

                diff_x = next_x - start_x
                diff_y = next_y - start_y

            except Exception:  # No path found
                # Means that we are very close to the player
                # just go straight to him
                center_x, center_y = self.center()
                diff_x = goal_center_x - center_x
                diff_y = goal_center_y - center_y

            if np.argmax([np.abs(diff_x), np.abs(diff_y)]) == 0:
                if diff_x > 0:
                    self.base_control = CONTROL_RIGHT
                elif diff_x < 0:
                    self.base_control = CONTROL_LEFT
            else:
                if diff_y > 0:
                    self.base_control = CONTROL_DOWN
                else:
                    self.base_control = CONTROL_TOP

        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)

        return self.base_control

    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.size_x, self.size_y = ENEMY_SIZE
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        self.think_is_x, self.think_is_y = self.x, self.y
        self.speed = ENEMY_SPEED
        self.goal_x = -1
        self.goal_y = -1
        self.player_seen = False
        self.base_control = CONTROL_RIGHT
        self.no_goal_dt = random.random() * 2
        self.color = "orange"
        self.path = []
        self.remember_player_dt = 0


    def see(self, dt):
        # Use to make the enemy remember that he saw the player and continue to seek him
        self.remember_player_dt -= dt

        # Use to compute the vision of the enemy
        player_x, player_y = self.board.player.center()
        player_tile_x, player_tile_y = get_tile_from_position(player_x, player_y)
        enemy_tile_x, enemy_tile_y = get_tile_from_position(self.x, self.y)

        # Distance in tile
        distance_player = np.sqrt(
            np.power(player_tile_x - enemy_tile_x, 2) + np.power(player_tile_y - enemy_tile_y, 2))

        tile_check = False

        # Here we gather all tile between the enemy and the player
        if distance_player > 1:

            # steps to take to reach the player
            diff_x, diff_y = (player_x - self.x) / (40*distance_player), (
                        player_y - self.y) / (40*distance_player)

            dist_x, dist_y = self.center()
            tile_x, tile_y = get_tile_from_position(dist_x, dist_y)

            # While the tile checked have not reached the player yet
            while abs(player_tile_x-enemy_tile_x) + abs(player_tile_y-enemy_tile_y) > abs(tile_x-enemy_tile_x) + abs(tile_y-enemy_tile_y):
                # We walk of one step
                dist_x += diff_x
                dist_y += diff_y
                # Get the tile and add it to the to check list
                tile_x, tile_y = get_tile_from_position(dist_x, dist_y)
                if 0 < tile_x <= self.board.size_x-1 and 0 < tile_y <= self.board.size_y-1 and (tile_x, tile_y):
                    # Here we check if the enemy can actually see the player (no wall between them)

                    if isinstance(self.board.board[tile_x][tile_y], Wall):
                        tile_check = True
                        break

        # If the enemy remembers the player or
        # If he sees him (no wall between) and if he is enough close
        # The enemy sees the player
        if self.remember_player_dt > 0 or (ENEMY_VIEW_DIST >= distance_player >= len(self.path) - 1 and not tile_check):
            self.color = "red"
            self.player_seen = True
            if self.remember_player_dt <= 0:
                self.remember_player_dt = ENEMY_MEMORY
        else:  # The enemy is not seeing the player
            self.color = "violet"
            self.player_seen = False

    def close_to_player(self):
        # Use to check if the enemy caught the player
        center_x, center_y = self.center()
        goal_center_x, goal_center_y = self.board.player.center()
        distance = np.sqrt(np.power(center_x - goal_center_x, 2) + np.power(center_y - goal_center_y, 2))
        return distance < 46

    def center(self):
        size_x, size_y = ENEMY_SIZE
        return self.x + size_x / 2, self.y + size_y / 2

    def move(self, control, dt):
        collision = super().move(control, dt)
        # If there is a collision we change the position used to compute the a star algorithm
        # Because an enemy can be blocked by a wall and not seeing it
        if collision and self.player_seen:
            self.think_is_x, self.think_is_y = collision
        else:
            self.think_is_x, self.think_is_y = self.center()

    def draw(self, canvas):
        self.rect = pygame.Rect(self.x, self.y, self.size_x, self.size_y)
        pygame.draw.rect(canvas, self.color, self.rect)
