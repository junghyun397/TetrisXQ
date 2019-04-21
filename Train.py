# -*- coding: utf-8 -*-
import argparse
import os
import random

import numpy as np
import tensorflow as tf

from Settings import Settings
from agent.dqn.QMLPModel import QMLPModel
from agent.dqn.data.BatchManager import BatchManager
from environment.AutoPlayEnvironment import AutoPlayEnvironment
from environment.ManualPlayEnvironment import ManualPlayer
from graphics.DummyGraphicModule import DummyGraphicModule
from graphics.GraphicModule import GraphicModule

SAVE_POINT = 20

LEARNING_EPOCH = 2000
MAX_TURNS = 100000

START_EPSILON = 1
MIN_EPSILON = 0.01

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env-type", help="Set environment type", type=str, default="auto")
parser.add_argument("-g", "--use-graphic", help="Using graphic interface", type=bool, default=True)
args = parser.parse_args()


def main(_):

    with tf.Session() as sess:
        settings = Settings()
        epsilon = START_EPSILON

        q_network_model = QMLPModel(settings)
        batch_module = BatchManager(settings)

        if args.use_graphic:
            graphic_interface = GraphicModule(settings)
        else:
            graphic_interface = DummyGraphicModule()

        if args.env_type == "manual":
            env_model = ManualPlayer(settings, graphic_interface)
        else:
            env_model = AutoPlayEnvironment(settings, graphic_interface)

        train_step = 0
        merged_summary = tf.summary.merge_all()
        writer = tf.summary.FileWriter('./train/log/train_log', sess.graph)

        init = tf.global_variables_initializer()
        sess.run(init)
        print("Start training: " + str(LEARNING_EPOCH) + " epoch...")
        for epoch in range(LEARNING_EPOCH):
            turn_count = 0
            current_end = False
            current_state = env_model.get_current_state()

            while not current_end:
                train_step += 1
                if turn_count > MAX_TURNS:
                    break

                if (float(random.randrange(0, 9999)) / 10000) <= epsilon:
                    action = random.randrange(0, settings.ACTIONS)
                else:
                    q_values = q_network_model.get_forward(sess, current_state)[0]
                    action = np.argmax(q_values)

                if epsilon > MIN_EPSILON:
                    epsilon = epsilon * 0.999

                next_state, reward, next_end = env_model.action(action)
                batch_module.add_data(current_state, next_state, action, reward)

                current_state = next_state
                current_end = next_end

                input_state, target_values = batch_module.get_batch(sess, q_network_model.get_target_value)
                summary, cost = q_network_model.optimize_step(sess, input_state, target_values, merged_summary)
                writer.add_summary(summary, train_step)
            print("epoch: " + str(epoch) + " global step: " + str(train_step) + " score: " + str(
                round(env_model.tetris_model.score)) +
                  " process turns: " + str(env_model.tetris_model.turns) + " exploration: " + str(round(epsilon * 100)))

            if epoch % SAVE_POINT == 0:
                print("Model saved: " + tf.train.Saver().save(sess,
                                                         os.getcwd() + "./train/saved_model/saved_model_DQN_TetrisXQ.ckpt"))

        writer.close()
        print("training finished: " + str(LEARNING_EPOCH) + "games.")


if __name__ == '__main__':
    tf.app.run()
