class TetrisModel:

    def __init__(self, settings):
        self._board_height = settings.GRID_HEIGHT
        self._board_width = settings.GRID_WIDTH

        self.board = None
        self.tetromino = settings.TETROMINO

        self.current_tetromino = None
        self.current_shape_code = 0
        self.current_rotate = 0
        self.current_score = 0

        self.is_end = False
        self.turns = 0
        self.score = 0

        self.clear_board()

    # Board

    def get_clear_board(self):
        return [0] * self._board_height * self._board_width

    def clear_board(self):
        self.board = self.get_clear_board()
        self.is_end = False
        self.turns = 0
        self.score = 0

        self.next_state(0)

    def next_state(self, shape_code):
        if self.is_end:
            self.clear_board()
            return

        self.turns += 1

        self.current_tetromino = self.tetromino.get_tetromino(shape_code, 0)
        self.current_shape_code = shape_code
        self.current_rotate = 0
        self.current_score = 0

    def get_board_data(self):
        return self.board[:]

    def get_board(self, y, x):
        return self.board[y * self._board_width + x]

    def set_board(self, y, x, v):
        self.board[y * self._board_width + x] = v

    # Move / Set

    def rotate_block(self, y, x):
        temp_rotate = self.current_rotate + 1
        if temp_rotate > self.tetromino.get_rotate_count(self.current_shape_code):
            temp_rotate = 0

        if self._can_update(y, x, self.tetromino.get_tetromino(self.current_shape_code, temp_rotate)):
            self.current_tetromino = self.tetromino.get_tetromino(self.current_shape_code, temp_rotate)
            self.current_rotate = temp_rotate
            return True
        return False

    def rotate_block_rate(self, y, x, rate):
        if self._can_update(y, x, self.tetromino.get_tetromino(self.current_shape_code, rate)):
            self.current_tetromino = self.tetromino.get_tetromino(self.current_shape_code, rate)
            self.current_rotate = rate
            return True
        return False

    def can_move_block(self, y, x):
        if self._can_update(y, x, self.current_tetromino):
            return True
        return False

    def sum_tetromino(self, y, x):
        self.board = self.get_sum_tetromino_board(y, x)
        self.update_board()

    def get_sum_tetromino_board(self, y, x):
        n_board = self.get_board_data()
        for col in range(len(self.current_tetromino)):
            for row in range(len(self.current_tetromino[0])):
                if self.get_board(y + col, x + row) == 0 and self.current_tetromino[col][row] == 1:
                    n_board[(y + col) * self._board_width + x + row] = 1
        return n_board

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
        self.board, removed_lines, filled_lines, append_lines = self.get_removed_board(self.board)

        if filled_lines == self._board_height:
            self.is_end = True

        self._update_score(removed_lines)

    def get_removed_board(self, board):
        removed_lines = 0
        filled_lines = 0
        append_lines = 0

        board = board[:]

        for index in range(self._board_height):
            line_sum = sum(board[index * self._board_width:(index + 1) * self._board_width])
            if line_sum == self._board_width:
                n_board = board[:]
                for z_index in range(self._board_width):
                    n_board[z_index] = 0
                for s_index in range(index * self._board_width):
                    n_board[self._board_width + s_index] = board[s_index]
                board = n_board
                removed_lines += 1
            elif line_sum > 0:
                if line_sum > 2:
                    append_lines += 1
                filled_lines += 1

        return board, removed_lines, filled_lines, append_lines

    def analysis_board(self, board):
        board, full, height, _ = self.get_removed_board(board)

        deep_hole = 0
        roof = 0

        def get_board(fy, fx):
            if fy >= self._board_height or fx >= self._board_width or fx < 0:
                return 1
            return board[fy * self._board_width + fx]

        for x in range(self._board_width):
            deep_hole_count = 0
            has_roof = False
            for y in range(self._board_height):
                if has_roof and get_board(y, x) == 0:
                    roof += 1
                elif get_board(y, x) == 1:
                    has_roof = True
                elif deep_hole_count == 0 and get_board(y, x) == 0 and get_board(y, x - 1) == 1 and get_board(y, x + 1) == 1:
                    deep_hole_count += 1
                elif deep_hole_count > 0:
                    if get_board(y, x) == 0:
                        deep_hole_count += 1
                    if deep_hole_count > 2:
                        deep_hole += 1

        return full, height, deep_hole, roof

    # Score

    def _update_score(self, removed_lines):
        self.current_score = abs(removed_lines ** 1.5 * 10)
        self.score += self.current_score
