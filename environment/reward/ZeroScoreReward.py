from environment.reward.RewardModule import RewardModule


class ZeroScoreReward(RewardModule):

    def get_reward(self, tetris_model):
        reward = 0

        if tetris_model.current_score == 0:
            reward = 1

        if tetris_model.is_end:
            reward = 100
        return reward
