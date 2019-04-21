from abc import ABCMeta, abstractmethod

import numpy as np

from tetris.TetrisModel import TetrisModel


class EnvironmentModel(metaclass=ABCMeta):

    def __init__(self, settings, graphic_module, reward_module):
        self._states = settings.STATES

        self.board_height = settings.GRID_HEIGHT
        self.board_width = settings.GRID_WIDTH

        self.tetris_model = TetrisModel(settings)
        self.graphic_module = graphic_module
        self.graphic_module.set_tetris_model(self.tetris_model)

        self.reward_module = reward_module

        self.end_point = 0

    def action(self, action) -> (np.ndarray, float, bool):
        self.tetris_model.next_state(action)
        self.do_action()
        return self.get_current_state(), self.reward_module.get_reward(self.tetris_model), self.tetris_model.is_end

    @abstractmethod
    def do_action(self):
        pass

    def get_current_state(self):
        return np.reshape(self.tetris_model.get_board_data(), (1, self._states))
