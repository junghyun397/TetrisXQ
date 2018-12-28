from abc import ABCMeta, abstractmethod

from tetris.TetrisModel import TetrisModel


class EnvironmentModel(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, settings):
        self._states = settings.STATES
        self.tetris_model = TetrisModel(settings)

    @abstractmethod
    def action_and_reward(self, action):
        pass

    def get_current_state(self):
        return self.tetris_model.get_board_data()

    def get_reward(self):
        reward = -1 * self.tetris_model.current_score * 0.05
        if self.tetris_model.is_end:
            reward = 1
        return reward
