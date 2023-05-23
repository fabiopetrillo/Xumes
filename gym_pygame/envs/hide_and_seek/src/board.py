import random
from os import walk
from typing import List

import numpy as np

from envs.hide_and_seek.params import TILE_SIZE, PLAYER_SIZE, NORMAL_GAME
from envs.hide_and_seek.src.entity import Entity
from envs.hide_and_seek.src.enemy import Enemy
from envs.hide_and_seek.src.ground import Ground
from envs.hide_and_seek.src.lidar import Lidar
from envs.hide_and_seek.src.player import Player
from envs.hide_and_seek.src.wall import Wall


def print_graph(graph):
    for tile in graph.keys():
        print(f"Node {tile.x}, {tile.y}")
        for tile_co in graph[tile]:
            print(tile_co.x, tile_co.y)


class Board:
    level_names = \
        next(walk("/home/cytech/Cours/ING2/IA 2/rl_project//gym_pygame/envs/hide_and_seek/src/maps"), (None, None, []))[
            2]

    def __init__(self, level):
        self.size_x, self.size_y = 20, 20
        self.board = np.ndarray((self.size_x, self.size_y), dtype=Wall)

        # Graphs are useful to compute the a-star algorithm
        self.ground_graph = {}
        self.reachable_ground_graph = {}
        self.wall_graph = {}

        self.enemies = []
        self.player = None
        self.lidar = None
        self.number_coins = 0
        self.level = level
        self.generate_world()

    def generate_world(self):

        if not NORMAL_GAME:
            normal_game = np.random.choice([True, False], p=[0.5, 0.5])
        else:
            normal_game = True

        # Create a board with just wall in it
        for i in range(self.size_x):
            for j in range(self.size_y):
                # For every tile create a board
                # And connect it in the graph
                wall = Wall(i, j, self)
                self.board[i][j] = wall
                if 0 < i < self.size_x - 1 and 0 < j < self.size_y - 1:
                    self.wall_graph[wall] = []
                    left = i - 1
                    top = j - 1
                    right = i + 1

                    # TODO refactor this part
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

        # Load map
        with open(
                f"/home/cytech/Cours/ING2/IA 2/rl_project/gym_pygame/envs/hide_and_seek/src/maps/map{self.level}") as f:
            lines = f.readlines()
            j = 0
            for line in lines:
                i = 0
                for value in line:
                    try:
                        v = int(value)
                        if v == 1 or v == 2 or v == 3 or v == 4:
                            self.remove_tile(self.wall_graph, i, j)

                            coin = False
                            if v == 2:
                                coin = True
                                if not normal_game:
                                    coin = np.random.choice([True, False], p=[0.8, 0.2])
                            ground = Ground(i, j, self.board, has_coin=coin)

                            if ground.has_coin:
                                self.number_coins += 1
                            self.add_tile(self.ground_graph, ground, i, j)
                            self.add_reachable_tile(self.reachable_ground_graph, ground, i, j)
                            if v == 3 and normal_game:
                                size_x, size_y = PLAYER_SIZE

                                # self.player = Player(i * TILE_SIZE - size_x // 2,
                                #                      j * TILE_SIZE - size_y // 2, self)

                                self.player = Player(i * TILE_SIZE, j * TILE_SIZE, self)
                            if v == 4 and normal_game:
                                self.enemies.append(Enemy(i * TILE_SIZE, j * TILE_SIZE, self))
                    except:
                        pass
                    i += 1
                j += 1

        # Determine the position of start of the player if not in file
        random_ground = None
        if not self.player:
            random_ground = np.random.choice(list(self.ground_graph.keys()))
            size_x, size_y = PLAYER_SIZE
            self.player = Player(random_ground.x * TILE_SIZE + np.random.randint(size_x + 1, TILE_SIZE - size_x - 1),
                                 random_ground.y * TILE_SIZE + np.random.randint(size_x + 1, TILE_SIZE - size_x - 1),
                                 self)
            # self.player = Player(random_ground.x * TILE_SIZE - size_x // 2 , random_ground.y * TILE_SIZE  - size_y // 2, self)

        if not normal_game:
            enemies_ground = list(self.ground_graph.keys()).copy()
            if random_ground:
                enemies_ground.remove(random_ground)
                for ground in self.ground_graph[random_ground]:
                    if ground in enemies_ground:
                        enemies_ground.remove(ground)
            random_ground_enemy = np.random.choice(enemies_ground)
            self.enemies.append(Enemy(random_ground_enemy.x * TILE_SIZE, random_ground_enemy.y * TILE_SIZE, self))

        self.lidar = Lidar(self, self.player)
        # Remove duplicates in every graphs
        for ground in self.ground_graph.keys():
            self.ground_graph[ground] = set(self.ground_graph[ground])
        for ground in self.reachable_ground_graph.keys():
            self.reachable_ground_graph[ground] = set(self.reachable_ground_graph[ground])
        for wall in self.wall_graph.keys():
            self.wall_graph[wall] = set(self.wall_graph[wall])

    def add_tile(self, graph, tile, x, y):
        # Add a tile in a board representation graph
        self.board[x][y] = tile
        graph[tile] = []
        # Connect to neighbor tiles
        for i in range(x - 1, x + 1):
            for j in range(y - 1, y + 1):
                if 0 < i < self.size_x - 1 and 0 < j < self.size_y - 1:
                    if isinstance(self.board[i][j], type(tile)):
                        graph[tile].append(self.board[i][j])
                        graph[self.board[i][j]].append(tile)

    def add_reachable_tile(self, graph, tile, x, y):
        # Add a tile in a board representation graph where
        # Connection are not in diagonal

        self.board[x][y] = tile
        graph[tile] = []

        left = x - 1
        right = x + 1
        top = y - 1
        bottom = y + 1

        self.add_tile_neighbors(graph, left, tile, y)
        self.add_tile_neighbors(graph, right, tile, y)
        self.add_tile_neighbors(graph, x, tile, top)
        self.add_tile_neighbors(graph, x, tile, bottom)

    def add_tile_neighbors(self, graph, checked_x, tile, checked_y):
        # Add tile to a determined neighbor
        if checked_x > 0 and checked_y > 0 and isinstance(self.board[checked_x][checked_y], type(tile)):
            graph[tile].append(self.board[checked_x][checked_y])
            if tile not in graph[self.board[checked_x][checked_y]]:
                graph[self.board[checked_x][checked_y]].append(tile)

    def remove_tile(self, graph, x, y):
        # Remove a tile from a graph
        # Disconnect from every neighbors
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
        # Remove the node
        if tile in graph.keys():
            graph.pop(tile)

    def count_ground_around(self, x, y):
        # Count how much ground there is around a tile
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

    def draw(self, canvas):
        # draw every tile on the board
        for row in self.board:
            for tile in row:
                if tile:
                    tile.draw(canvas)
                    if isinstance(tile, Ground):
                        tile.color = "green"
                    else:
                        tile.color = "gray"

        for enemy in self.enemies:
            enemy.draw(canvas)

        self.lidar.draw(canvas)
        self.lidar.logs(canvas)
        self.player.draw(canvas)
        self.player.logs(canvas)

    def compute_state(self, dt):
        self.player.control(dt)
        self.player.check_if_coin()
        self.lidar.vision()
        if self.check_no_more_coins():
            if self.level + 1 < len(self.level_names):
                self.__init__(self.level + 1)
            else:
                self.reset(0)
        if self.is_caught_by_enemy(dt):
            self.reset(0)

    def is_caught_by_enemy(self, dt):
        for enemy in self.enemies:
            enemy.control(dt)
            enemy.see(dt)
            if enemy.close_to_player():
                return True
        return False

    @property
    def entities(self):
        entities: List[Entity] = []
        entities.extend(self.enemies)
        entities.append(self.player)
        return entities

    def print_board(self):
        for row in self.board:
            for tile in row:
                if isinstance(tile, Wall):
                    print("1 ", end="")
                else:
                    print("  ", end="")
            print()

    def check_no_more_coins(self):
        # If the player won the game
        if self.player.points >= self.number_coins:
            return True

    def reset(self, level):
        self.__init__(level=level)
