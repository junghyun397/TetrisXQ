
class Tetromino(object):

    _TETROMINO_PIECE = dict()
    _TETROMINO_PIECE['N'] = [[[0]]]
    _TETROMINO_PIECE['I'] = [[[1, 1, 1, 1]], [[1], [1], [1], [1]]]
    _TETROMINO_PIECE['O'] = [[[1, 1], [1, 1]]]
    _TETROMINO_PIECE['T'] = [[[1, 1, 1], [0, 1, 0]], [[1, 0], [1, 1], [1, 0]], [[0, 1, 0], [1, 1, 1]], [[0, 1], [1, 1], [0, 1]]]
    _TETROMINO_PIECE['J'] = [[[1, 1, 1, 1], [0, 0, 0, 1]], [[1, 1], [1, 0], [1, 0], [1, 0]], [[1, 0, 0, 0], [1, 1, 1, 1]], [[0, 1], [0, 1], [0, 1], [1, 1]]]
    _TETROMINO_PIECE['L'] = [[[1, 1, 1, 1], [1, 0, 0, 0]], [[1, 0], [1, 0], [1, 0], [1, 1]], [[0, 0, 0, 1], [1, 1, 1, 1]], [[1, 1], [0, 1], [0, 1], [0, 1]]]
    _TETROMINO_PIECE['S'] = [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]]
    _TETROMINO_PIECE["Z"] = [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]]

    _TETROMINO_ROTATE = dict()
    _TETROMINO_ROTATE['N'] = 1
    _TETROMINO_ROTATE['I'] = 2
    _TETROMINO_ROTATE['T'] = 1
    _TETROMINO_ROTATE['J'] = 4
    _TETROMINO_ROTATE['L'] = 4
    _TETROMINO_ROTATE['S'] = 2
    _TETROMINO_ROTATE["Z"] = 2

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
