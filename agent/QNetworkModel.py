from abc import ABCMeta


class DeepQNetworkModel(metaclass=ABCMeta):

    def optimize_step(self, sess, x, y):
        pass

    def get_forward(self, sess, x):
        pass

    def get_target_value(self, sess, input_state, next_state, action, reward):
        pass

    def get_target_update_value(self, reward, max_q):
        pass
