from tetris.Tetromino import Tetromino


class TetrisModel:

    def __init__(self, settings):
        self.board_width = settings['gridWidth']
        self.board_height = settings['gridHeight']

        self._board = [0] * self.board_width * self.board_height

        self._now_shape_code = 'N'
        self._now_rotate = 0
        self._now_tetromino = Tetromino.get_tetromino(self._now_shape_code, self._now_rotate)

