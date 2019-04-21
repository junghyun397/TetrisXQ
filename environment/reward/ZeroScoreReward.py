from environment.reward.RewardModule import RewardModule


class ZeroScoreReward(RewardModule):

    def __init__(self):
        super().__init__()

    def get_reward(self, tetris_model):

        if tetris_model.current_score == 0:
            reward = 1
        else:
            reward = 0

        if tetris_model.is_end:
            reward = 100
        return reward
