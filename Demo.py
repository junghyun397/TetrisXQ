import argparse

import numpy as np
import tensorflow as tf

from Settings import Settings
from agent.dqn.QMLPModel import QMLPModel
from environment.AutoPlayEnvironment import AutoPlayEnvironment
from environment.ManualPlayEnvironment import ManualPlayer
from graphics.DummyGraphicModule import DummyGraphicModule
from graphics.GraphicModule import GraphicModule

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env-type", help="Set environment type", type=str, default="auto")
parser.add_argument("-g", "--use-graphic", help="Using graphic interface", type=bool, default=True)
args = parser.parse_args()


def main(_):

    with tf.Session() as sess:
        settings = Settings()

        q_network_model = QMLPModel(settings)

        if args.use_graphic:
            graphic_interface = GraphicModule(settings)
        else:
            graphic_interface = DummyGraphicModule()

        if args.env_type == "manual":
            env_model = ManualPlayer(settings, graphic_interface)
        else:
            env_model = AutoPlayEnvironment(settings, graphic_interface)

        saver = tf.train.import_meta_graph("train/saved_model/saved_model_TetrisXQ.ckpt.meta")
        saver.restore(sess, tf.train.latest_checkpoint('./train/saved_model/'))

        current_state = env_model.get_current_state()

        init = tf.global_variables_initializer()
        sess.run(init)
        while True:
            q_values = q_network_model.get_forward(sess, current_state)[0]
            action = np.argmax(q_values)
            current_state, _, _ = env_model.action_and_reward(action)


if __name__ == '__main__':
    tf.app.run()
