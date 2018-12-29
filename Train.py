import os
import random

import tensorflow as tf
import numpy as np

from Settings import Settings
from agent.model.QMLPModel import QMLPModel
from agent.data.BatchManager import BatchManager
from display.DummyGraphicModule import DummyGraphicModule
from display.GraphicModule import GraphicModule
from display.HumanPlayer import HumanPlayer
from tetris.ai.TetrisAI import TetrisAI


USE_LOG = True
USE_GRAPHIC_INTERFACE = True
ENVIRONMENT_TYPE = 'HUMAN'


class TrainInfo:

    def __init__(self, settings):
        self.current_epoch = 0
        self.total_epoch = settings.LEARNING_EPOCH


def main(_):
    settings = Settings()

    epsilon = settings.START_EPSILON

    tf.set_random_seed(settings.RAND_SEED)

    with tf.Session() as sess:
        writer = tf.summary.FileWriter('./board/train_log', sess.graph)

        train_info = TrainInfo(settings)

        q_network_model = QMLPModel(settings)
        batch_model = BatchManager(settings)
        graphic_interface = DummyGraphicModule()
        if USE_GRAPHIC_INTERFACE:
            graphic_interface = GraphicModule(settings, train_info)
        if ENVIRONMENT_TYPE == 'HUMAN':
            env_model = HumanPlayer(settings, graphic_interface)
        else:
            env_model = TetrisAI(settings, graphic_interface)

        init = tf.global_variables_initializer()
        sess.run(init)

        for index in range(settings.LEARNING_EPOCH):
            error = 0
            current_end = False
            current_state = env_model.get_current_state()

            max_q = 0
            turn_count = 0

            while not current_end:
                if (float(random.randrange(0, 9999)) / 10000) <= epsilon:
                    action = random.randrange(0, settings.ACTIONS)
                else:
                    q_values = q_network_model.get_forward(sess, current_state)[0]
                    print(q_values)
                    action = np.argmax(q_values)

                    if q_values[action] > max_q:
                        max_q = q_values[action]

                if epsilon > settings.MIN_EPSILON:
                    epsilon = epsilon * 0.999

                next_state, reward, next_end = env_model.action_and_reward(action)
                batch_model.add_data(current_state, next_state, action, reward)

                current_state = next_state
                current_end = next_end

                input_state, target_values = batch_model.get_batch(sess, q_network_model.get_target_value)
                loss = q_network_model.optimize_step(sess, input_state, target_values)
                error += loss

                turn_count += 1

            train_info.current_epoch = index + 1
            print("순번: " + str(index) + " 최대 Q: " + str(max_q) + " 진행 턴 수: " + str(turn_count) +
                  " 무작위 행동: " + str(round(epsilon * 100)) + " 전체 손실: " + str(error))

        tf.train.Saver().save(sess, os.getcwd() + "./model/saved_model_TetrisXQ.ckpt")


if __name__ == '__main__':
    tf.app.run()
