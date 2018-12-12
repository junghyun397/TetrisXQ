from abc import ABCMeta


class DeepQNetworkModel(metaclass=ABCMeta):

    def optimize_one_step(self, sess, x, y):
        pass

    def get_target_q_value(self, sess, input_state, next_state, action, reward):
        pass

    def get_target_y(self, reward, max_q):
        pass

    def get_q_value(self, sess, x):
        pass
