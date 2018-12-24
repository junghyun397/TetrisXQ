from abc import ABCMeta, abstractmethod

import numpy as np

from tetris.TetrisModel import TetrisModel


class EnvironmentModel(metaclass=ABCMeta):

    def __init__(self, settings):
        self._states = settings.STATES
        self.tetris_model = TetrisModel(settings)

    @abstractmethod
    def action_and_reward(self, action):
        pass

    def get_vector_state(self):
        return np.reshape(self.tetris_model.get_board(), (1, self._states))

    def get_reward(self):
        append_height = 0
        return (append_height * 0.1) + (self.tetris_model.current_score * 0.01)
