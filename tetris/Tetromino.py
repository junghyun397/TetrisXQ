
class Tetromino(object):

    TETROMINO_I = 0
    TETROMINO_O = 1
    TETROMINO_T = 2
    TETROMINO_J = 3
    TETROMINO_L = 4
    TETROMINO_S = 5
    TETROMINO_Z = 6

    _TETROMINO_PIECE = [
        [[[1, 1, 1, 1]], [[1], [1], [1], [1]]],
        [[[1, 1], [1, 1]]],
        [[[1, 1, 1], [0, 1, 0]], [[1, 0], [1, 1], [1, 0]], [[0, 1, 0], [1, 1, 1]], [[0, 1], [1, 1], [0, 1]]],
        [[[1, 1, 1, 1], [0, 0, 0, 1]], [[1, 1], [1, 0], [1, 0], [1, 0]], [[1, 0, 0, 0], [1, 1, 1, 1]], [[0, 1], [0, 1], [0, 1], [1, 1]]],
        [[[1, 1, 1, 1], [1, 0, 0, 0]], [[1, 0], [1, 0], [1, 0], [1, 1]], [[0, 0, 0, 1], [1, 1, 1, 1]], [[1, 1], [0, 1], [0, 1], [0, 1]]],
        [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]],
        [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]]
    ]

    _TETROMINO_ROTATE = [1, 0, 0, 3, 3, 1, 1]

    @staticmethod
    def get_tetromino(code, rotate):
        return Tetromino._TETROMINO_PIECE[code][rotate]

    @staticmethod
    def get_tetromino_size(code, rotated):
        return len(Tetromino._TETROMINO_PIECE[code][rotated][0]), len(Tetromino._TETROMINO_PIECE[code][rotated])

    @staticmethod
    def get_tetromino_all():
        return Tetromino._TETROMINO_PIECE

    @staticmethod
    def get_rotate_count(code):
        return Tetromino._TETROMINO_ROTATE[code]
