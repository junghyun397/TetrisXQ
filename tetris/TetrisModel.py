import numpy

from tetris.Tetromino import Tetromino


class TetrisModel:

    def __init__(self, settings):
        self._board_width = settings.GRID_WIDTH
        self._board_height = settings.GRID_HEIGHT

        self.board = None

        self.current_tetromino = None
        self.current_shape_code = 0
        self.current_rotate = 0

        self.current_score = 0
        self.current_append_height = 0

        self.is_end = False
        self.score = 0

        self.clear_board()

    # Board

    def clear_board(self):
        self.board = numpy.zeros((self._board_height, self._board_width))

        self.current_tetromino = Tetromino.get_tetromino(0, 0)
        self.current_shape_code = 0
        self.current_rotate = 0

        self.current_score = 0
        self.current_append_height = 0

        self.is_end = False
        self.score = 0

    def next_state(self, shape_code):
        self.current_tetromino = Tetromino.get_tetromino(shape_code, 0)
        self.current_shape_code = shape_code
        self.current_rotate = 0

        self.current_score = 0
        self.current_append_height = 0

    def update_board(self):
        removed_lines = 0
        filled_lines = 0
        new_board = numpy.zeros((self._board_height, self._board_width))

        for index in range(self._board_height):
            if numpy.sum(self.board[index]) == self._board_width:
                new_board[0] = [0] * self._board_width
                for n_index in range(self._board_height - 1):
                    if n_index + 1 != index:
                        new_board[n_index + 1] = self.board[n_index]
                removed_lines += 1
            elif numpy.amax(self.board[index]) == 1:
                filled_lines += 1

        if removed_lines > 0:
            self.board = new_board

        if filled_lines == self._board_height:
            self.is_end = True

        self._update_score(removed_lines)

    def get_board_data(self):
        return self.board[:]

    # Move / Set

    def can_update(self, y, x, shape):
        for i in range(len(shape)):
            for o in range(len(shape[0])):
                if self.board[y + i][x + o] == 1 and shape[i][o] == 1:
                    return False
        return True

    def rotate_block(self, y, x):
        temp_rotate = 0
        if temp_rotate + 1 > Tetromino.get_rotate_count(self.current_shape_code):
            temp_rotate = 0
        else:
            temp_rotate += 1

        if self.can_update(y, x, Tetromino.get_tetromino(self.current_shape_code, temp_rotate)):
            for i in range(len(self.current_tetromino)):
                for o in range(len(self.current_tetromino[0])):
                    self.board[y + i][x + o] = 1
            self.current_rotate = temp_rotate
            return True
        return False

    def set_block(self, y, x):
        if self.can_update(y, x, self.current_tetromino):
            for i in range(len(self.current_tetromino)):
                for o in range(len(self.current_tetromino[0])):
                    self.board[y + i][x + o] = 1
            return True
        return False

    # Score

    def _update_score(self, removed_lines):
        self.current_append_height = removed_lines
        self.current_score = abs(removed_lines ** 1.5 * 10)
        self.score += self.current_score

        if self.is_end:
            self.current_score = 0
            self.score = 0
