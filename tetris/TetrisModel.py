import numpy

from tetris.Tetromino import Tetromino


class TetrisModel:

    def __init__(self, settings):
        self._board_width = settings.GRID_WIDTH
        self._board_height = settings.GRID_HEIGHT

        self._board = None

        self._current_tetromino = None
        self._current_shape_code = 0
        self._current_rotate = 0

        self.current_score = 0
        self.current_append_height = 0

        self.is_end = False
        self.score = 0

        self.clear_board()

    # Board

    def clear_board(self):
        self._board = numpy.zeros((self._board_width, self._board_height))

        self._current_tetromino = Tetromino.get_tetromino(0, 0)
        self._current_shape_code = 0
        self._current_rotate = 0

        self.current_score = 0
        self.current_append_height = 0

        self.is_end = False
        self.score = 0

    def next_state(self, shape_code):
        self._current_tetromino = Tetromino.get_tetromino(shape_code, 0)
        self._current_shape_code = shape_code
        self._current_rotate = 0

        self.current_score = 0
        self.current_append_height = 0

    def update_board(self):
        removed_lines = 0
        for i in range(self._board_height):
            if numpy.sum(self._board[i]) == self._board_width:
                pass
        self._update_score(removed_lines)

    def get_board(self):
        return self._board

    # Move / Set

    def can_move(self, x, y):
        pass

    def can_rotate(self, x, y):
        pass

    def rotate_block(self):
        if self._current_rotate + 1 > Tetromino.get_rotate_count(self._current_shape_code):
            self._current_rotate = 0
        self._current_rotate += 1

    def set_block(self, x, y):
        for i in range(len(self._current_tetromino)):
            for o in range(len(self._current_tetromino[0])):
                self._board[y + o][x + i] = 1

    # Score

    def _update_score(self, removed_lines):
        self.current_append_height = removed_lines
        self.current_score += abs(removed_lines ** 1.5 * 10)
        self.score += self.current_score
