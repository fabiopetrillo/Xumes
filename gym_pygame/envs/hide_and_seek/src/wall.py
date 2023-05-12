from envs.hide_and_seek.src.tile import Tile


class Wall(Tile):

    def __init__(self, x, y, board):
        super().__init__(x, y, board, "gray")

