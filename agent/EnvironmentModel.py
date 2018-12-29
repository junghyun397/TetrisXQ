from abc import ABCMeta, abstractmethod

import numpy as np

from tetris.TetrisModel import TetrisModel


class EnvironmentModel(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, settings, graphic_module):
        self._states = settings.STATES
        self.tetris_model = TetrisModel(settings)
        self.graphic_module = graphic_module
        self.graphic_module.set_tetris_model(self.tetris_model)

    @abstractmethod
    def action_and_reward(self, action):
        pass

    def get_current_state(self):
        return np.reshape(self.tetris_model.get_board_data(), (1, self._states))

    def get_reward(self):
        reward = 0
        reward += -1 * self.tetris_model.current_score * 0.5
        reward += self.tetris_model.current_append_height * 0.1
        return reward
