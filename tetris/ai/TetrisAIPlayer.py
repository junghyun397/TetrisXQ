from agent.EnvironmentModel import EnvironmentModel
from tetris.Tetromino import Tetromino
from tetris.ai.TetrisAI import TetrisAI
from tetris.ai.Weight import Weight


class TetrisAIPlayer(EnvironmentModel, TetrisAI):

    def __init__(self, settings, graphic_module):
        EnvironmentModel.__init__(self, settings, graphic_module)
        TetrisAI.__init__(self, settings, self.tetris_model)

        self._base_weight = Weight()
        self._opt_weight = Weight()
        self._weight = Weight()

        self._opt_weight.WEIGHT_FULL = 50
        self._opt_weight.WEIGHT_POST_FLOOR = 5
        self._opt_weight.WEIGHT_HEIGHT = -10
        self._opt_weight.WEIGHT_DEEP_HOLE = -0.1
        self._opt_weight.WEIGHT_ROOF = -0.1

        self._prv_block = -1
        self._prv_block_count = 0

        self._is_opt_mode = False

    def do_action(self):
        self._update_policy(self.tetris_model.current_shape_code)

        chosen_state, _ = self.get_evaluated_states()

        if chosen_state is None:
            self.tetris_model.is_end = True
            self.graphic_module.draw_graphic(-1, -1)
        else:
            _, y, x, rotate, _, _ = chosen_state
            self.tetris_model.rotate_block_rate(y, x, rotate)
            self.graphic_module.draw_graphic(y, x)
            self.tetris_model.sum_tetromino(y, x)

        self.graphic_module.pump_event()

    def get_state_list(self):
        states = dict()

        num_index = 0
        rotate_count = Tetromino.get_rotate_count(self.tetris_model.current_shape_code) + 1
        for rotate_rate in range(rotate_count):
            for x in range(self.board_width):
                if self.tetris_model.rotate_block_rate(0, x, rotate_rate):
                    dy = 0
                    while self.tetris_model.can_move_block(dy + 1, x):
                        dy += 1

                    def check_pos(fy, fx):
                        return fy >= self.board_height or fx >= self.board_width or fx < 0 or self.tetris_model.get_board(fy, fx) == 1

                    post_floor = 0
                    post_side = 0
                    for col in range(len(self.tetris_model.current_tetromino)):
                        for row in range(len(self.tetris_model.current_tetromino[0])):
                            if self.tetris_model.current_tetromino[col][row] == 1:
                                if check_pos(dy + col, x + row - 1):
                                    post_side += 1
                                if check_pos(dy + col, x + row + 1):
                                    post_side += 1
                                if check_pos(dy + col + 1, x + row):
                                    post_floor += 1

                    states[num_index] = self.tetris_model.get_sum_tetromino_board(dy, x), dy, x, rotate_rate, post_side, post_floor
                    num_index += 1
        return states

    def _update_policy(self, block):
        if block == self._prv_block:
            self._prv_block_count += 1
            if self._prv_block_count > 3:
                self._weight = self._opt_weight
                self._is_opt_mode = True
        else:
            self._prv_block_count = 0
            if self._is_opt_mode:
                self._weight = self._base_weight
                self._is_opt_mode = False
        self._prv_block = block
