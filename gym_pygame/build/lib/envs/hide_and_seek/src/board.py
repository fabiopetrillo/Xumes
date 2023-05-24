import random
from typing import List

import numpy as np

from envs.hide_and_seek.params import TILE_SIZE, PLAYER_SIZE, BOARD_SIZE
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
    def __init__(self):
        self.size_x, self.size_y = BOARD_SIZE
        self.board = np.ndarray((self.size_x, self.size_y), dtype=Wall)

        # Graphs are useful to compute the a-star algorithm
        self.ground_graph = {}
        self.reachable_ground_graph = {}
        self.wall_graph = {}

        self.enemies = []
        self.player = None
        self.lidar = None
        self.number_coins = 0
        self.generate_world()

    def generate_world(self):

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

        # Get a start for the creation of the ground
        i_start = np.random.randint(1, self.size_x - 1)
        j_start = np.random.randint(1, self.size_y - 1)

        # Add a ground at this position
        self.remove_tile(self.wall_graph, i_start, j_start)
        ground = Ground(i_start, j_start, self.board, has_coin=np.random.choice([False, True]))
        if ground.has_coin:
            self.number_coins += 1
        self.add_tile(self.ground_graph, ground, i_start, j_start)
        self.add_reachable_tile(self.reachable_ground_graph, ground, i_start, j_start)

        # Use a random method to create other ground tiles
        for k in range(max(self.size_x, self.size_y)):
            changes = []
            for tile in self.wall_graph.keys():
                i = tile.x
                j = tile.y
                # We count the number of ground around and determine with a random choice if we replace
                # it by a ground
                count = self.count_ground_around(i, j)
                transform = 0.40 * np.sin(count)
                rand = random.random()
                if rand < transform:
                    changes.append((i, j))

            # Then we compute the changes (replacing wall by grounds)
            for i, j in changes:
                self.remove_tile(self.wall_graph, i, j)
                ground = Ground(i, j, self.board, has_coin=np.random.choice([False, True], p=[0.9, 0.1]))
                if ground.has_coin:
                    self.number_coins += 1
                self.add_tile(self.ground_graph, ground, i, j)
                self.add_reachable_tile(self.reachable_ground_graph, ground, i, j)

        random_ground = np.random.choice(list(self.ground_graph.keys()))
        size_x, size_y = PLAYER_SIZE
        self.player = Player(random_ground.x * TILE_SIZE + np.random.randint(size_x + 1, TILE_SIZE - size_x - 1),
                             random_ground.y * TILE_SIZE + np.random.randint(size_x + 1, TILE_SIZE - size_x - 1),
                             self)

        enemies_ground = list(self.ground_graph.keys()).copy()
        if random_ground:
            enemies_ground.remove(random_ground)
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
            self.reset()
        if self.is_caught_by_enemy(dt):
            self.reset()

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

    def reset(self):
        self.__init__()