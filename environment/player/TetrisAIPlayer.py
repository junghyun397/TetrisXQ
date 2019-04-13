from environment.EnvironmentModel import EnvironmentModel
from tetris.ai.TetrisAI import TetrisAI
from tetris.ai.TetrisWeight import TetrisWeight


class TetrisAIPlayer(EnvironmentModel, TetrisAI):

    def __init__(self, settings, graphic_module):
        EnvironmentModel.__init__(self, settings, graphic_module)
        TetrisAI.__init__(self, settings, self.tetris_model)

        self._base_weight = TetrisWeight()
        self._opt_weight = TetrisWeight()
        self._weight = TetrisWeight()

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
