from abc import ABCMeta

import numpy as np

from tetris.TetrisModel import TetrisModel


class EnvironmentModel(metaclass=ABCMeta):

    def __init__(self, settings):
        self._nbStates = settings['nbStates']
        self._tetris_model = TetrisModel(settings)

    def action_and_reward(self, action):
        pass

    def get_vector_state(self):
        return np.reshape(self._tetris_model.get_board(), (1, self._nbStates))
