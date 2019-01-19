from abc import ABCMeta, abstractmethod

import numpy as np

from tetris.TetrisModel import TetrisModel


class EnvironmentModel(metaclass=ABCMeta):

    def __init__(self, settings, graphic_module):
        self._states = settings.STATES

        self.board_height = settings.GRID_HEIGHT
        self.board_width = settings.GRID_WIDTH

        self.tetris_model = TetrisModel(settings)
        self.graphic_module = graphic_module
        self.graphic_module.set_tetris_model(self.tetris_model)

        self.end_point = 0

        self._prv_height = 0
        self._prv_deep_hole = 0
        self._prv_roof = 0

        self._prv_action = -1
        self._action_count = 0
        self._action_correction_weight = 0

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)
        self._action_correction(action)
        self.do_action()
        return self.get_current_state(), self.get_reward(), self.tetris_model.is_end

    @abstractmethod
    def do_action(self):
        pass

    def get_current_state(self):
        return np.reshape(self.tetris_model.get_board_data(), (1, self._states))

    def get_reward(self):
        reward = 0
        reward += -0.5 * self.tetris_model.current_score

        _, height, deep_hole, roof = self.tetris_model.analysis_board(self.tetris_model.board)
        reward += max(0, height - self._prv_height) * 2
        reward += max(0, deep_hole - self._prv_deep_hole) * 5
        reward += max(0, roof - self._prv_roof) * 5
        reward += self._action_correction_weight

        self._action_correction_weight = 0
        self._prv_height = height
        self._prv_deep_hole = deep_hole
        self._prv_roof = roof

        if self.tetris_model.is_end:
            reward = 1000
        return reward

    def _action_correction(self, action):
        if self._prv_action == action:
            self._action_count += 1
            if self._action_count > 10:
                self._action_correction_weight = min(1000, round(1.2 ** self._action_count)) * -1
        else:
            self._action_count = 0
        self._prv_action = action
