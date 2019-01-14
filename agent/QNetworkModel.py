from abc import ABCMeta, abstractmethod


class DeepQNetworkModel(metaclass=ABCMeta):

    @abstractmethod
    def optimize_step(self, sess, x, y, summary):
        pass

    @abstractmethod
    def get_forward(self, sess, x):
        pass

    @abstractmethod
    def get_target_value(self, sess, input_state, next_state, action, reward):
        pass
