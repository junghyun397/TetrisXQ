from tetris.TetrominoInterface import TetrominoInterface


class Tetromino(TetrominoInterface):

    TETROMINO_I = 0
    TETROMINO_O = 1
    TETROMINO_T = 2
    TETROMINO_J = 3
    TETROMINO_L = 4
    TETROMINO_S = 5
    TETROMINO_Z = 6

    def __init__(self):
        self._TETROMINO_PIECE = [
            [[[1, 1, 1, 1]], [[1], [1], [1], [1]]],  # I, 0
            [[[1, 1], [1, 1]]],  # O, 1
            [[[1, 1, 1], [0, 1, 0]], [[1, 0], [1, 1], [1, 0]], [[0, 1, 0], [1, 1, 1]], [[0, 1], [1, 1], [0, 1]]],  # T, 2
            [[[1, 1, 1], [0, 0, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 0, 0], [1, 1, 1]], [[0, 1], [0, 1], [1, 1]]],  # J, 3
            [[[1, 1, 1], [1, 0, 0]], [[1, 0], [1, 0], [1, 1]], [[0, 0, 1], [1, 1, 1]], [[1, 1], [0, 1], [0, 1]]],  # L, 4
            [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]],  # S, 5
            [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]]  # Z, 6
        ]

        self._TETROMINO_ROTATE = [1, 0, 3, 3, 3, 1, 1]

    def get_tetromino(self, code, rotate):
        return self._TETROMINO_PIECE[code][rotate]

    def get_tetromino_size(self, code, rotated):
        return len(self._TETROMINO_PIECE[code][rotated][0]), len(self._TETROMINO_PIECE[code][rotated])

    def get_tetromino_all(self):
        return self._TETROMINO_PIECE

    def get_rotate_count(self, code):
        return self._TETROMINO_ROTATE[code]
