import numpy as np

from agent.EnvironmentModel import EnvironmentModel
from tetris.Tetromino import Tetromino

WEIGHT_FULL = 3000
WEIGHT_WALL = 1
WEIGHT_FLAT = 2

WEIGHT_HEIGHT = -10
WEIGHT_HOLE = 0
WEIGHT_DEEP_HOLE = -5
WEIGHT_DOT = -3


class TetrisAI(EnvironmentModel):

    def __init__(self, settings, graphic_module):
        super().__init__(settings, graphic_module)

        self._def_height = 0
        self._def_walls = 0
        self._def_flat = 0

        self._def_holes = 0
        self._def_deep_holes = 0
        self._def_apertures = 0

    def do_action(self):
        max_score = 0
        chosen_state = None

        states = self._get_state_list()
        for state in states:
            board, y, x, rotate_rate = state
            board, full_line, height, f_height = self.tetris_model.analysis_board(board)
            wall, hole, deep_hole, dot = self.tetris_model.analysis_board(state)

            score = 0
            if score > max_score:
                max_score = score
                chosen_state = state

        if chosen_state is None:
            self.tetris_model.is_end = True
        else:
            board, _, _, _ = chosen_state
            self.tetris_model.board = board

    def _get_state_list(self):
        states = dict()

        num_index = 0
        rotate_count = Tetromino.get_rotate_count(self.tetris_model.current_shape_code) + 1
        for rotate_rate in range(rotate_count):
            for x in range(self.board_width):
                if self.tetris_model.rotate_block_rate(0, x, rotate_rate):
                    dy = 0
                    while self.tetris_model.can_move_block(dy, x):
                        dy += 1
                    states[num_index] = self.tetris_model.get_sum_tetromino_board(dy, x), dy, x, rotate_rate
                    num_index += 1
        return states
