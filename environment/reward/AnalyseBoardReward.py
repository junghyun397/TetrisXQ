from environment.reward.RewardModule import RewardModule


class AnalyseBoardReward(RewardModule):

    def __init__(self):
        super().__init__()
        self._prv_height = 0
        self._prv_deep_hole = 0
        self._prv_roof = 0

    def get_reward(self, tetris_model):
        reward = -1
        reward += -0.01 * tetris_model.current_score
        reward += -0.01 * tetris_model.turns

        _, height, deep_hole, roof = tetris_model.analysis_board(tetris_model.board)
        reward += 2 * max(0, height - self._prv_height)
        reward += 5 * max(0, deep_hole - self._prv_deep_hole)
        reward += 5 * max(0, roof - self._prv_roof)

        self._prv_height = height
        self._prv_deep_hole = deep_hole
        self._prv_roof = roof

        if tetris_model.is_end:
            self._reset_prv_info()
            reward = 100
        return reward

    def _reset_prv_info(self):
        self._prv_height = 0
        self._prv_deep_hole = 0
        self._prv_roof = 0
