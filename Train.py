# -*- coding: utf-8 -*-
import os
import random

import numpy as np
import tensorflow as tf

from Settings import Settings
from agent.data.BatchManager import BatchManager
from agent.model.QMLPModel import QMLPModel
from display.DummyGraphicModule import DummyGraphicModule
from display.GraphicModule import GraphicModule
from display.HumanPlayer import HumanPlayer
from tetris.ai.TetrisAI import TetrisAI

SAVE_POINT = 20
USE_GRAPHIC_INTERFACE = True
ENVIRONMENT_TYPE = 'AI'


class TrainInfo:

    def __init__(self, settings):
        self.current_epoch = 0
        self.total_epoch = settings.LEARNING_EPOCH


def main(_):
    settings = Settings()

    epsilon = settings.START_EPSILON

    with tf.Session() as sess:
        train_info = TrainInfo(settings)

        q_network_model = QMLPModel(settings)
        batch_module = BatchManager(settings)
        graphic_interface = DummyGraphicModule()
        if USE_GRAPHIC_INTERFACE:
            graphic_interface = GraphicModule(settings, train_info)
        if ENVIRONMENT_TYPE == 'HUMAN':
            env_model = HumanPlayer(settings, graphic_interface)
        else:
            env_model = TetrisAI(settings, graphic_interface)

        train_step = 0
        merged_summary = tf.summary.merge_all()
        writer = tf.summary.FileWriter('./train/log/train_log', sess.graph)

        init = tf.global_variables_initializer()
        sess.run(init)
        print("훈련 시작: " + str(settings.LEARNING_EPOCH) + " 게임 학습...")
        for index in range(settings.LEARNING_EPOCH):
            turn_count = 0
            current_end = False
            current_state = env_model.get_current_state()

            while not current_end:
                if turn_count >= settings.MAX_TURNS:
                    break

                if (float(random.randrange(0, 9999)) / 10000) <= epsilon:
                    action = random.randrange(0, settings.ACTIONS)
                else:
                    q_values = q_network_model.get_forward(sess, current_state)[0]
                    action = np.argmax(q_values)

                if epsilon > settings.MIN_EPSILON:
                    epsilon = epsilon * 0.999

                next_state, reward, next_end = env_model.action_and_reward(action)
                batch_module.add_data(current_state, next_state, action, reward)

                current_state = next_state
                current_end = next_end

                input_state, target_values = batch_module.get_batch(sess, q_network_model.get_target_value)
                summary, cost = q_network_model.optimize_step(sess, input_state, target_values, merged_summary)
                writer.add_summary(summary, train_step)
                train_step += 1
                turn_count += 1

            train_info.current_epoch = index + 1
            print("epoch: " + str(train_info.current_epoch) + " 전체 step: " + str(train_step) +
                  " 진행 턴 수: " + str(turn_count) + " 무작위 행동: " + str(round(epsilon * 100)))

            if train_info.current_epoch % SAVE_POINT == 0:
                print("모델 저장됨: " + tf.train.Saver().save(sess, os.getcwd() + "./train/saved_model/saved_model_TetrisXQ.ckpt"))

        writer.close()
        print("훈련 종료: " + str(settings.LEARNING_EPOCH) + " 게임 학습 완료")


if __name__ == '__main__':
    tf.app.run()
