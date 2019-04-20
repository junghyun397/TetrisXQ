from environment.EnvironmentModel import EnvironmentModel
from environment.reward.AnalyseBoardReward import AnalyseBoardReward
from graphics.DummyGraphicModule import DummyGraphicModule
from tetris.ai.TetrisAI import TetrisAI
from tetris.ai.TetrisWeight import TetrisWeight


class TetrisAIEnvironment(EnvironmentModel, TetrisAI):

    def __init__(self, settings, graphic_module=DummyGraphicModule(), reward_module=AnalyseBoardReward()):
        EnvironmentModel.__init__(self, settings, graphic_module, reward_module)
        TetrisAI.__init__(self, settings, self.tetris_model)

        self._base_weight = TetrisWeight()
        self._weight = TetrisWeight()
        self._opt_weight = TetrisWeight(weight_full=50, weight_post_floor=5, weight_height=-10, weight_deep_hole=-0.1, weight_roof=-0.1)

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
