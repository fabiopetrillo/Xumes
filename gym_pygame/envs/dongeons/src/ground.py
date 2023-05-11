from envs.dongeons.src.tile import Tile


class Ground(Tile):

    def __init__(self, x, y, board):
        super().__init__(x, y, board, "green")
