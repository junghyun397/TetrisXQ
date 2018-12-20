import os
import random

import tensorflow as tf

import Settings
from agent.model.QMLPModel import QMLPModel
from agent.data.BatchManager import BatchManager
from tetris.ai.TetrisAI import TetrisAI


def main(_):

    settings = Settings.settings

    rand_rate = 1

    tf.set_random_seed(settings['randSeed'])

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        writer = tf.summary.FileWriter('./board/train_log', sess.graph)

        q_network_model = QMLPModel(settings)
        batch_model = BatchManager(settings)
        env_model = TetrisAI(settings)

        for index in range(settings['epoch']):
            error = 0
            current_end = False
            current_state = env_model.get_vector_state()

            max_q = 0
            turn_count = 0

            while not current_end:
                turn_count += 1
                if (float(random.randrange(0, 9999)) / 10000) <= rand_rate:
                    action = random.randrange(0, settings['nbActions'])
                else:
                    q_values = q_network_model.get_forward(sess, current_state)
                    action = q_values.argmax()

                    if q_values[action] > max_q:
                        max_q = q_values[action]

                if rand_rate > 0.0001:
                    rand_rate = rand_rate * 0.99

                next_state, reward, next_end = env_model.action_and_reward(action)
                batch_model.add_data(current_state, next_state, action, reward)

                current_state = next_state
                current_end = next_end

                input_state, target_values = batch_model.get_batch(sess, q_network_model.get_target_value)
                loss = q_network_model.optimize_step(sess, input_state, target_values)
                error = error + loss

                writer.add_summary(loss)
                writer.add_summary(error)
                writer.add_summary(max_q)

            writer.add_summary(turn_count)
            print("순번: " + str(index) + " 최대 Q: " + max_q + " 진행 턴 수: " + turn_count + " 무작위 행동: " + rand_rate * 100
                  + " 전체 손실: " + error)

        tf.train.Saver().save(sess, os.getcwd() + "./model/saved_model_TetrisXQ.ckpt")


if __name__ == '__main__':
    tf.app.run()
