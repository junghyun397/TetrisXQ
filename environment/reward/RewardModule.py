from abc import ABCMeta, abstractmethod


class RewardModule(metaclass=ABCMeta):

    @abstractmethod
    def get_reward(self, tetris_model):
        pass
