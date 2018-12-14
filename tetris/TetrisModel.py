from tetris.Tetromino import Tetromino


class TetrisModel:

    def __init__(self, settings):
        self.board_width = settings['gridWidth']
        self.board_height = settings['gridHeight']

        self._board = None
        self._now_shape_code = None
        self._now_rotate = None
        self._now_tetromino = None

        self._current_core = 0

        self.clear_board()

    # Board

    def clear_board(self):
        self._board = [0] * self.board_width * self.board_height

        self._now_shape_code = 'N'
        self._now_rotate = 0
        self._now_tetromino = Tetromino.get_tetromino(self._now_shape_code, self._now_rotate)

    def update_board(self):
        pass

    def get_board(self):
        return self._board

    # Move / Set

    def can_move(self, x, y):
        pass

    def set_block(self):
        pass

    # Score

    def update_score(self, removed_lines):
        pass

    def get_score(self):
        return self._current_core
