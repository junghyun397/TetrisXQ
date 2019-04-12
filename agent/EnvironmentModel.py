from abc import ABCMeta, abstractmethod

import numpy as np

from agent.model.RewardType import RewardType
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

        self._max_turn = 0

        if settings.REWARD_MODE == RewardType.BY_ANALYSE_BOARD:
            def new_rwd():
                reward = -1
                reward += -0.01 * self.tetris_model.current_score
                reward += -0.01 * self.tetris_model.turns

                _, height, deep_hole, roof = self.tetris_model.analysis_board(self.tetris_model.board)
                reward += 2 * max(0, height - self._prv_height)
                reward += 5 * max(0, deep_hole - self._prv_deep_hole)
                reward += 5 * max(0, roof - self._prv_roof)
                reward += self._action_correction_weight

                self._action_correction_weight = 0
                self._prv_height = height
                self._prv_deep_hole = deep_hole
                self._prv_roof = roof

                if self.tetris_model.is_end:
                    reward = 100
                return reward
            self.get_reward = new_rwd
        elif settings.REWARD_MODE == RewardType.BY_ZERO_SCORE:
            def new_rwd():
                reward = 0

                if self.tetris_model.current_score == 0:
                    reward = 1

                self._action_correction_weight = 0

                if self.tetris_model.is_end:
                    reward = 100
                return reward
            self.get_reward = new_rwd
        elif settings.REWARD_MODE == RewardType.BY_SUM_TURNS:
            def new_rwd():

                if self._max_turn < self.tetris_model.turns:
                    reward = (self.tetris_model.turns - self._max_turn) * 15
                    self._max_turn = self.tetris_model.turns
                else:
                    reward = (self.tetris_model.turns / self._max_turn) * 100

                return reward
            self.get_reward = new_rwd

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)
        self.do_action()
        self._action_correction(action)
        return self.get_current_state(), self.get_reward(), self.tetris_model.is_end

    @abstractmethod
    def do_action(self):
        pass

    def get_current_state(self):
        return np.reshape(self.tetris_model.get_board_data(), (1, self._states))

    # noinspection PyMethodMayBeStatic
    def get_reward(self):
        return 0

    def _action_correction(self, action):
        if self._prv_action == action:
            self._action_count += 1
            if self._action_count > 8:
                self._action_correction_weight = -1 * min(50, round(1.2 ** self._action_count))
        else:
            self._action_count = 0
        self._prv_action = action
