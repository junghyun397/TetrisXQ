import math
import numpy as np
import tensorflow as tf

from Settings import Settings
from agent.DeepNetworkModel import DeepNetworkModel


class QCNNModel(DeepNetworkModel):

    def __init__(self, settings=Settings(),
                 hidden_size=300,
                 discount=0.8,
                 learning_rate=0.05):
        self._hidden_size = hidden_size
        self._discount = discount
        self._learning_rate = learning_rate

        self._grid_height = settings.GRID_HEIGHT
        self._grid_width = settings.GRID_WIDTH

        self._states = settings.STATES
        self._actions = settings.ACTIONS

        self._build_model()
        self._build_optimizer()

    # Model Builder

    def _build_model(self):

        self.X = tf.placeholder(tf.float32, [None, self._grid_height, self._grid_width])
        self.Y = tf.placeholder(tf.float32, [None, self._actions])

        with tf.name_scope("layer_conv_1"):
            W1 = tf.Variable(tf.random_normal([4, 4, 1, 16], stddev=0.01))
            hidden_layer_1 = tf.nn.conv2d(self.X, W1, strides=[1, 1, 1, 1], padding='SAME')
            hidden_layer_1 = tf.nn.leaky_relu(hidden_layer_1, 0.1)
            hidden_layer_1 = tf.nn.max_pool(hidden_layer_1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

        with tf.name_scope("layer_conv_2"):
            W2 = tf.Variable(tf.random_normal([4, 4, 16, 32], stddev=0.01))
            hidden_layer_2 = tf.nn.conv2d(hidden_layer_1, W2, strides=[1, 1, 1, 1], padding='SAME')
            hidden_layer_2 = tf.nn.leaky_relu(hidden_layer_2, 0.1)
            hidden_layer_2 = tf.nn.max_pool(hidden_layer_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
            hidden_layer_2 = tf.reshape(hidden_layer_2, [-1, 44])

        with tf.name_scope("layer_3"):
            W3 = tf.Variable(tf.truncated_normal([44, self._hidden_size],
                                                 stddev=1.0 / math.sqrt(float(self._hidden_size))))
            b3 = tf.Variable(tf.truncated_normal([self._hidden_size], stddev=0.01))
            hidden_layer_3 = tf.nn.leaky_relu(tf.matmul(hidden_layer_2, W3) + b3, 0.1)
            tf.summary.histogram("fc_layer_3_weight", W3)

        with tf.name_scope("layer_4"):
            W4 = tf.Variable(tf.truncated_normal([self._hidden_size, self._actions],
                                                 stddev=1.0 / math.sqrt(float(self._hidden_size))))
            b4 = tf.Variable(tf.truncated_normal([self._actions], stddev=0.01))
            self.output_layer = tf.matmul(hidden_layer_3, W4) + b4
            tf.summary.histogram("fc_layer_4_weight", W4)

    def _build_optimizer(self):
        with tf.name_scope("cost"):
            self.cost = tf.losses.mean_squared_error(self.Y, self.output_layer)
            tf.summary.scalar("cost", self.cost)
        with tf.name_scope("train"):
            self.optimizer = tf.train.AdamOptimizer(self._learning_rate).minimize(self.cost)

    # Model Function

    def optimize_step(self, sess, x, y, summary):
        x = np.reshape(x, (self._grid_height, self._grid_width))
        return sess.run([summary, self.cost], feed_dict={self.X: x, self.Y: y})

    def get_forward(self, sess, x):
        x = np.reshape(x, (self._grid_height, self._grid_width))
        return sess.run(self.output_layer, feed_dict={self.X: x})

    def get_target_value(self, sess, input_state, next_state, action, reward):
        target_q_values = self.get_forward(sess, input_state)
        next_q_values = self.get_forward(sess, next_state)
        next_max_q = np.amax(next_q_values)

        target_q_values[0, [action]] = reward + next_max_q * self._discount

        return input_state[0], target_q_values[0]
