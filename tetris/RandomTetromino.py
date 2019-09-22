import random

from tetris.TetrominoInterface import TetrominoInterface


class RandomTetromino(TetrominoInterface):

    def build_tetromino(self, size=20, max_width=4, max_height=4):
        rs = []
        for _ in range(size):
            width = random.randint(3, max_width)
            rs.append([[random.randint(0, 1) for _ in range(width)] for _ in range(random.randint(2, max_height))])
        return rs
