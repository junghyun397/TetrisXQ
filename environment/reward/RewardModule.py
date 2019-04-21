from abc import ABCMeta, abstractmethod


class RewardModule(metaclass=ABCMeta):

    def __init__(self, game_end_reward=100):
        self.game_end_reward = game_end_reward

    @abstractmethod
    def get_reward(self, tetris_model):
        pass
