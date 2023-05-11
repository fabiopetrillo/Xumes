import random
from abc import ABC
from typing import Optional, Dict, List

import numpy as np
import pygame

from envs.dongeons.params import ENEMY_SIZE, ENEMY_VIEW_DIST, TILE_SIZE
from envs.dongeons.src.Entity import Entity, CONTROL_DOWN, CONTROL_TOP, CONTROL_LEFT, CONTROL_RIGHT, \
    get_tile_from_position
from envs.dongeons.src.tile import Tile
from envs.dongeons.src.utils.PriorityQueue import PriorityQueue


def heuristic(a: Tile, b: Tile) -> float:
    (x1, y1) = a.x, a.y
    (x2, y2) = b.x, b.y

    return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))
    # return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from: Dict[Tile, Tile],
                     start: Tile, goal: Tile) -> List[Tile]:
    current: Tile = goal
    path: List[Tile] = []
    if goal not in came_from:  # no path was found
        return []

    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()  # optional
    return path


def a_star_search(graph: dict, start: Tile, goal: Tile):
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

    def attack(self):
        pass

    def find_control(self, dt):
        if not self.close_to_player():
            if not self.player_seen:
                self.no_goal_dt -= dt
                if self.no_goal_dt <= 0:
                    self.no_goal_dt = random.random() * 2
                    self.base_control = np.random.choice([CONTROL_RIGHT, CONTROL_LEFT, CONTROL_TOP, CONTROL_DOWN])
            else:
                center_x, center_y = self.think_is_x, self.think_is_y
                goal_center_x, goal_center_y = self.board.player.center()
                start_ground_x, start_ground_y = get_tile_from_position(center_x, center_y)
                start = self.board.get_ground_from_position(start_ground_x, start_ground_y)
                goal_x, goal_y = get_tile_from_position(goal_center_x, goal_center_y)
                goal = self.board.get_ground_from_position(goal_x, goal_y)
                came_from, cost_so_far = a_star_search(self.board.reachable_ground_graph, start, goal)
                path = reconstruct_path(came_from, start, goal)
                try:
                    collision_x, collision_y = get_tile_from_position(center_x, center_y)
                    start = self.board.get_ground_from_position(collision_x, collision_y)

                    next_pos = path[0]
                    start_x, start_y = start.x, start.y

                    next_x, next_y = next_pos.x, next_pos.y
                    # print(start_x, start_y, next_x, next_y)

                    diff_x = next_x - start_x
                    diff_y = next_y - start_y
                    # print(diff_x, diff_y, len(cost_so_far))
                    if diff_x > 0:
                        self.base_control = CONTROL_RIGHT
                    elif diff_x < 0:
                        self.base_control = CONTROL_LEFT
                    elif diff_y > 0:
                        self.base_control = CONTROL_DOWN
                    else:
                        self.base_control = CONTROL_TOP
                except Exception:
                    pass

        return self.base_control

    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.size_x, self.size_y = ENEMY_SIZE
        self.think_is_x, self.think_is_y = self.x, self.y
        self.speed = 100
        self.goal_x = -1
        self.goal_y = -1
        self.player_seen = False
        self.base_control = CONTROL_RIGHT
        self.no_goal_dt = random.random() * 2
        self.color = "black"

    def see(self):
        player_x, player_y = self.board.player.x, self.board.player.y
        distance_player = np.sqrt(np.power(self.x - player_x, 2) + np.power(self.y - player_y, 2))
        if distance_player <= ENEMY_VIEW_DIST:
            self.color = "red"
            self.player_seen = True
        else:
            self.color = "black"
            self.player_seen = False

    def close_to_player(self):
        center_x, center_y = self.center()
        goal_center_x, goal_center_y = self.board.player.center()
        distance = np.sqrt(np.power(center_x - goal_center_x, 2) + np.power(center_y - goal_center_y, 2))
        return distance < 5

    def center(self):
        size_x, size_y = ENEMY_SIZE

        return self.x + size_x / 2, self.y + size_y / 2

    def move(self, control, dt):
        collision = super().move(control, dt)
        if collision and self.player_seen:
            self.think_is_x, self.think_is_y = collision
        else:
            self.think_is_x, self.think_is_y = self.center()
    def draw(self, canvas):
        size_x, size_y = ENEMY_SIZE
        rect_bottom = pygame.Rect(self.x, self.y, size_x, size_y)
        pygame.draw.rect(canvas, self.color, rect_bottom)
