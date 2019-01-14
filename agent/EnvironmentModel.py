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

        self._prv_height = 0
        self._prv_deep_hole = 0
        self._prv_roof = 0

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)
        self.do_action()
        return self.get_current_state(), self.get_reward(), self.tetris_model.is_end

    @abstractmethod
    def do_action(self):
        pass

    def get_current_state(self):
        return np.reshape(self.tetris_model.get_board_data(), (1, self._states))

    def get_reward(self):
        reward = 0
        reward += -1 * self.tetris_model.current_score

        _, height, deep_hole, roof = self.tetris_model.analysis_board(self.tetris_model.board)
        reward += max(0, height - self._prv_height) * 0.1
        reward += max(0, deep_hole - self._prv_deep_hole) * 0.5
        reward += max(0, roof - self._prv_roof) * 0.5

        self._prv_height = height
        self._prv_deep_hole = deep_hole
        self._prv_roof = roof

        if self.tetris_model.is_end:
            reward = 100
        return reward
