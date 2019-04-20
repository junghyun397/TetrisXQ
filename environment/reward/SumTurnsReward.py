from environment.reward.RewardModule import RewardModule


class SumTurnsReward(RewardModule):

    def __init__(self):
        self._max_turn = 0

    def get_reward(self, tetris_model):
        if self._max_turn < tetris_model.turns:
            reward = (tetris_model.turns - self._max_turn) * 15
            self._max_turn = tetris_model.turns
        else:
            reward = (tetris_model.turns / self._max_turn) * 100

        return reward
