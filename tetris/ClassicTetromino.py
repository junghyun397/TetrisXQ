from tetris.TetrominoInterface import TetrominoInterface


class ClassicTetromino(TetrominoInterface):

    def build_tetromino(self):
        return [
            [[1, 1, 1, 1]],  # I, 0
            [[1, 1], [1, 1]],  # O, 1
            [[1, 1, 1], [0, 1, 0]],  # T, 2
            [[1, 1, 1], [0, 0, 1]],  # J, 3
            [[1, 1, 1], [1, 0, 0]],  # L, 4
            [[0, 1, 1], [1, 1, 0]],  # S, 5
            [[1, 1, 0], [0, 1, 1]]  # Z, 6
        ]
