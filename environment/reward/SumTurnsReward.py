from environment.reward.RewardModule import RewardModule


class SumTurnsReward(RewardModule):

    def __init__(self):
        super().__init__()
        self._min_turn = 0

    def get_reward(self, tetris_model):
        if not tetris_model.is_end:
            reward = 0
        elif self._min_turn > tetris_model.turns:
            reward = (self._min_turn - tetris_model.turns) * 10
            self._min_turn = tetris_model.turns
        else:
            reward = ((self._min_turn + 0.01) / tetris_model.turns) * 10

        return reward
