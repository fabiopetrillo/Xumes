import random

import numpy as np

from envs.dongeons.params import BOARD_SIZE, TILE_SIZE
from envs.dongeons.src.enemy import Enemy
from envs.dongeons.src.ground import Ground
from envs.dongeons.src.player import Player
from envs.dongeons.src.tile import Tile
from envs.dongeons.src.wall import Wall


class Board:
    size_x, size_y = BOARD_SIZE
    board = np.ndarray(BOARD_SIZE, dtype=Wall)
    ground_graph = {}
    reachable_ground_graph = {}
    wall_graph = {}
    enemies = []
    player = None

    def add_tile(self, graph, tile, x, y):
        self.board[x][y] = tile
        graph[tile] = []
        for i in range(x - 1, x + 1):
            for j in range(y - 1, y + 1):
                if 0 < i < self.size_x - 1 and 0 < j < self.size_y - 1:
                    if isinstance(self.board[i][j], type(tile)):
                        graph[tile].append(self.board[i][j])
                        graph[self.board[i][j]].append(tile)

    def add_reachable_tile(self, graph, tile, x, y):
        self.board[x][y] = tile
        graph[tile] = []

        left = x - 1
        right = x + 1
        top = y - 1
        bottom = y + 1

        if left > 0 and isinstance(self.board[left][y], type(tile)):
            graph[tile].append(self.board[left][y])
            if tile not in graph[self.board[left][y]]:
                graph[self.board[left][y]].append(tile)
        if right < self.size_x - 1 and isinstance(self.board[right][y], type(tile)):
            graph[tile].append(self.board[right][y])
            if tile not in graph[self.board[right][y]]:
                graph[self.board[right][y]].append(tile)
        if top > 0 and isinstance(self.board[x][top], type(tile)):
            graph[tile].append(self.board[x][top])
            if tile not in graph[self.board[x][top]]:
                graph[self.board[x][top]].append(tile)
        if bottom < self.size_y and isinstance(self.board[x][bottom], type(tile)):
            graph[tile].append(self.board[x][bottom])
            if tile not in graph[self.board[x][bottom]]:
                graph[self.board[x][bottom]].append(tile)

    def remove_tile(self, graph, x, y):
        tile = self.board[x][y]
        for i in range(x - 1, x + 1):
            for j in range(y - 1, y + 1):
                if 0 < i < self.size_x - 1 and 0 < j < self.size_y - 1:
                    if isinstance(self.board[i][j], type(tile)):
                        if self.board[i][j] in graph.keys():
                            if tile in graph[self.board[i][j]]:
                                graph[self.board[i][j]].remove(tile)
                        else:
                            graph[self.board[i][j]] = []
        if tile in graph.keys():
            graph.pop(tile)

    def count_wall_around(self, x, y):
        count = 0
        left = x - 1
        right = x + 1
        top = y - 1
        bottom = y + 1

        if left > 0 and isinstance(self.board[left][y], Ground):
            count += 1
        if right < self.size_x - 1 and isinstance(self.board[right][y], Ground):
            count += 1
        if top > 0 and isinstance(self.board[x][top], Ground):
            count += 1
        if bottom < self.size_y and isinstance(self.board[x][bottom], Ground):
            count += 1

        return count

    def get_ground_from_position(self, x, y):
        for ground in self.reachable_ground_graph.keys():
            if ground.x == x and ground.y == y:
                return ground

    def __init__(self):
        for i in range(self.size_x):
            for j in range(self.size_y):
                wall = Wall(i, j, self)
                self.board[i][j] = wall
                if 0 < i < self.size_x - 1 and 0 < j < self.size_y - 1:
                    self.wall_graph[wall] = []
                    left = i - 1
                    top = j - 1
                    right = i + 1
                    if left != 0:
                        if isinstance(self.board[left][j], Wall):
                            self.wall_graph[wall].append(self.board[left][j])
                            self.wall_graph[self.board[left][j]].append(wall)
                    if top != 0:
                        if isinstance(self.board[i][top], Wall):
                            self.wall_graph[wall].append(self.board[i][top])
                            self.wall_graph[self.board[i][top]].append(wall)
                    if top != 0 and left != 0:
                        if isinstance(self.board[left][top], Wall):
                            self.wall_graph[wall].append(self.board[left][top])
                            self.wall_graph[self.board[left][top]].append(wall)
                    if top != 0 and right != self.size_y - 1:
                        if isinstance(self.board[right][top], Wall):
                            self.wall_graph[wall].append(self.board[right][top])
                            self.wall_graph[self.board[right][top]].append(wall)

        i_start = np.random.randint(1, self.size_x - 1)
        j_start = np.random.randint(1, self.size_y - 1)

        self.remove_tile(self.wall_graph, i_start, j_start)
        ground = Ground(i_start, j_start, self.board)
        self.add_tile(self.ground_graph, ground, i_start, j_start)
        self.add_reachable_tile(self.reachable_ground_graph, ground, i_start, j_start)
        for k in range(max(self.size_x, self.size_y)):
            changes = []
            for i in range(self.size_x):
                for j in range(self.size_y):
                    if 0 < i < self.size_x - 1 and 0 < j < self.size_y - 1 and isinstance(self.board[i][j], Wall):

                        count = self.count_wall_around(i, j)
                        transform = 0.40 * np.sin(count)
                        rand = random.random()
                        if rand < transform:
                            changes.append((i, j))

            for i, j in changes:
                self.remove_tile(self.wall_graph, i, j)
                ground = Ground(i, j, self.board)
                self.add_tile(self.ground_graph, ground, i, j)
                self.add_reachable_tile(self.reachable_ground_graph, ground, i, j)

        random_ground = np.random.choice(list(self.ground_graph.keys()))

        self.player = Player(random_ground.x * TILE_SIZE, random_ground.y * TILE_SIZE, self)

        for ground in self.ground_graph.keys():
            self.ground_graph[ground] = set(self.ground_graph[ground])
        for ground in self.reachable_ground_graph.keys():
            self.reachable_ground_graph[ground] = set(self.reachable_ground_graph[ground])
        for wall in self.wall_graph.keys():
            self.wall_graph[wall] = set(self.wall_graph[wall])

        # nb_enemies =
        nb_enemies = 1
        for i in range(nb_enemies):
            random_ground_enemy = np.random.choice(list(self.ground_graph.keys()))
            if random_ground_enemy != random_ground:
                self.enemies.append(Enemy(random_ground_enemy.x * TILE_SIZE, random_ground_enemy.y * TILE_SIZE, self))

    def draw(self, canvas):
        for row in self.board:
            for tile in row:
                if tile:
                    tile.draw(canvas)
                    if isinstance(tile, Ground):
                        tile.color = "green"
        for enemy in self.enemies:
            enemy.draw(canvas)
        self.player.draw(canvas)

    def compute_state(self, dt):
        self.player.control(dt)

        for enemy in self.enemies:
            enemy.control(dt)
            enemy.see()

    def print_graph(self, graph):
        for tile in graph.keys():
            print(f"Node {tile.x}, {tile.y}")
            for tile_co in graph[tile]:
                print(tile_co.x, tile_co.y)

    def print_board(self):
        for row in self.board:
            for tile in row:
                if isinstance(tile, Wall):
                    print("1 ", end="")
                else:
                    print("  ", end="")
            print()
