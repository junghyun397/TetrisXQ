import os
import random

import tensorflow as tf

from agent.TetrisXQModel import TetrisXQModel
from agent.data.BatchManager import BatchManager
from training_ai.TetrisAI import TetrisAI

settings = dict()
settings['randSeed'] = 503
settings['epoch'] = 2000

settings['nbActions'] = 7
settings['nbStates'] = 10 * 22
settings['hiddenSize'] = 100

settings['discount'] = 0.9
settings['learningRate'] = 0.001

settings['batchSize'] = 50
settings['maxMemory'] = 100


def main(_):

    rand_rate = 1

    tf.set_random_seed(settings['randSeed'])

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        writer = tf.summary.FileWriter('./board/train_log', sess.graph)

        tetrisXQ_model = TetrisXQModel(settings)
        batch_model = BatchManager(settings)
        env_model = TetrisAI()

        for index in range(settings['epoch']):
            error = 0
            current_end = False
            current_state = env_model.get_environment()

            max_q = 0
            turn_count = 0

            while not current_end:
                turn_count += 1
                if (float(random.randrange(0, 9999)) / 10000) <= rand_rate:
                    action = random.randrange(0, settings['nbActions'])
                else:
                    q_values = tetrisXQ_model.get_q_value(sess, current_state)
                    action = q_values.argmax()

                    if q_values[action] > max_q:
                        max_q = q_values[action]

                if rand_rate > 0.0001:
                    rand_rate = rand_rate * 0.99

                next_state, reward, next_end = env_model.action_and_reward(action)
                batch_model.add_data(current_state, next_state, action, reward)

                current_state = next_state
                current_end = next_end

                current_q_values, target_q_values = batch_model.get_batch(sess, tetrisXQ_model.get_target_q_value)
                loss = tetrisXQ_model.optimize_one_step(sess, current_q_values, target_q_values)
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
