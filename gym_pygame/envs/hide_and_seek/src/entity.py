from abc import abstractmethod, ABC

from envs.hide_and_seek.params import TILE_SIZE
from envs.hide_and_seek.src.wall import Wall

CONTROL_TOP = "top"
CONTROL_DOWN = "down"
CONTROL_RIGHT = "right"
CONTROL_LEFT = "left"

RIGHT = "right"
LEFT = "left"
TOP = "top"
DOWN = "bottom"


def get_tile_from_position(x, y):
    return int(x // TILE_SIZE), int(y // TILE_SIZE)


def check_collision_with_enemy(x, y, enemy):
    # check if point x, y is in the enemy
    return enemy.x <= x <= enemy.x + enemy.size_x and enemy.y <= y <= enemy.y + enemy.size_y


class Entity(ABC):

    def __init__(self, x, y, board):
        self.direction = RIGHT
        self.attack_dt = 0
        self.x = x
        self.y = y
        self.size_x, self.size_y = 0, 0
        self.board = board
        self.speed = 150

    @abstractmethod
    def find_control(self, dt):
        # Method used to make the entity return a control [CONTROL_TOP, CONTROL_DOWN, CONTROL_LEFT, CONTROL_RIGHT]
        # Here is where the entity is "thinking"
        raise NotImplementedError

    def control(self, dt):
        self.move(self.find_control(dt), dt)

    def move(self, control, dt):
        # Compute the control and check if collision
        new_position_y = self.y
        new_position_x = self.x

        if control == CONTROL_TOP:
            self.direction = TOP
            new_position_y = self.y - self.speed * dt
            # New position to check
            positions_to_check = [(self.x + self.size_x, new_position_y), (new_position_x, new_position_y)]
            # Last position corresponding to the corners checked
            corners = [(self.x + self.size_x, self.y), (self.x, self.y)]

        elif control == CONTROL_DOWN:
            self.direction = DOWN
            new_position_y = self.y + self.speed * dt
            positions_to_check = [(self.x + self.size_x, new_position_y + self.size_y),
                                  (new_position_x, new_position_y + self.size_y)]
            corners = [(self.x + self.size_x, self.y + self.size_x), (self.x, self.y + self.size_y)]

        elif control == CONTROL_LEFT:
            self.direction = LEFT
            new_position_x = self.x - self.speed * dt
            positions_to_check = [(new_position_x, self.y + self.size_y), (new_position_x, new_position_y)]
            corners = [(self.x, self.y + self.size_y), (self.x, self.y)]

        elif control == CONTROL_RIGHT:
            self.direction = RIGHT
            new_position_x = self.x + self.speed * dt
            positions_to_check = [(new_position_x + self.size_x, self.y + self.size_y),
                                  (new_position_x + self.size_x, new_position_y)]
            corners = [(self.x + self.size_x, self.y + self.size_y), (self.x + self.size_x, self.y)]

        else:
            positions_to_check = []
            corners = []

        # We check if there is not a wall in the new position or an entity
        # If there is something blocking we return the position of the corner that blocks
        for ((x, y), (corner_x, corner_y)) in zip(positions_to_check, corners):
            tile_x, tile_y = get_tile_from_position(x, y)
            if isinstance(self.board.board[tile_x][tile_y], Wall):
                return corner_x, corner_y
            for entity in self.board.entities:
                if check_collision_with_enemy(x, y, entity):
                    return corner_x, corner_y

        # No problem we compute the move
        self.y = new_position_y
        self.x = new_position_x

    def center(self):
        return self.x + self.size_x / 2, self.y + self.size_y / 2

    @abstractmethod
    def draw(self, canvas):
        raise NotImplementedError
