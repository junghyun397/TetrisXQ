import numpy as np

from tetris.Tetromino import Tetromino


class TetrisModel:

    def __init__(self, settings):
        self._board_height = settings.GRID_HEIGHT
        self._board_width = settings.GRID_WIDTH

        self.board = None

        self.current_tetromino = None
        self.current_shape_code = 0
        self.current_rotate = 0
        self.current_score = 0

        self.current_append_height = 0

        self._prv_height = 0

        self.is_end = False
        self.score = 0

        self.clear_board()

    # Board

    def get_clear_board(self):
        return [0] * self._board_height * self._board_width

    def clear_board(self):
        self.board = self.get_clear_board()
        self.is_end = False
        self.score = 0

        self._prv_height = 0

        self.next_state(0)

    def next_state(self, shape_code):
        if self.is_end:
            self.clear_board()
            return

        self.current_tetromino = Tetromino.get_tetromino(shape_code, 0)
        self.current_shape_code = shape_code
        self.current_rotate = 0
        self.current_score = 0

        self.current_append_height = 0

    def get_board_data(self):
        return self.board[:]

    def get_board(self, y, x):
        return self.board[y * self._board_width + x]

    def set_board(self, y, x, v):
        self.board[y * self._board_width + x] = v

    # Move / Set

    def rotate_block(self, y, x):
        temp_rotate = self.current_rotate + 1
        if temp_rotate > Tetromino.get_rotate_count(self.current_shape_code):
            temp_rotate = 0

        if self._can_update(y, x, Tetromino.get_tetromino(self.current_shape_code, temp_rotate)):
            self.current_tetromino = Tetromino.get_tetromino(self.current_shape_code, temp_rotate)
            self.current_rotate = temp_rotate
            return True
        return False

    def can_move_block(self, y, x):
        if self._can_update(y, x, self.current_tetromino):
            return True
        return False

    def sum_tetromino(self, y, x):
        for col in range(len(self.current_tetromino)):
            for row in range(len(self.current_tetromino[0])):
                if self.get_board(y + col, x + row) == 0 and self.current_tetromino[col][row] == 1:
                    self.set_board(y + col, x + row, 1)
        self.update_board()

    def _can_update(self, y, x, shape):
        if y > self._board_height or x < 0 or y + len(shape) > self._board_height or x + len(shape[0]) > self._board_width:
            return False
        for col in range(len(shape)):
            for row in range(len(shape[0])):
                if self.get_board(y + col, x + row) == 1 and shape[col][row] == 1:
                    return False
        return True

    # Sum board

    def update_board(self):
        removed_lines = 0
        filled_lines = 0
        append_lines = 0

        for index in range(self._board_height):
            line_sum = np.sum(self.board[index * self._board_width:(index + 1) * self._board_width])
            if line_sum == self._board_width:
                new_board = self.get_board_data()
                for z_index in range(self._board_width):
                    new_board[z_index] = 0
                for s_index in range(index * self._board_width):
                    new_board[self._board_width + s_index] = self.board[s_index]
                self.board = new_board
                removed_lines += 1
            elif line_sum > 0:
                if line_sum > 2:
                    append_lines += 1
                filled_lines += 1

        self.current_append_height = self._prv_height - append_lines
        self._prv_height = append_lines

        if filled_lines == self._board_height:
            self.is_end = True

        self._update_score(removed_lines)

    # Score

    def _update_score(self, removed_lines):
        self.current_score = abs(removed_lines ** 1.5 * 10)
        self.score += self.current_score

        if self.is_end:
            self.current_score = 0
            self.score = 0
