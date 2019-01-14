import numpy as np
import tensorflow as tf

import Train
from Settings import Settings
from agent.model.QMLPModel import QMLPModel
from display.DummyGraphicModule import DummyGraphicModule
from display.GraphicModule import GraphicModule
from display.HumanPlayer import HumanPlayer
from tetris.ai.TetrisAI import TetrisAI

USE_GRAPHIC_INTERFACE = True
ENVIRONMENT_TYPE = "HUMAN"


def main(_):
    settings = Settings()

    with tf.Session() as sess:
        train_info = Train.TrainInfo(settings)

        q_network_model = QMLPModel(settings)
        graphic_module = DummyGraphicModule()
        if USE_GRAPHIC_INTERFACE:
            graphic_module = GraphicModule(settings, train_info)
        if ENVIRONMENT_TYPE == "HUMAN":
            env_model = HumanPlayer(settings, graphic_module)
        else:
            env_model = TetrisAI(settings, graphic_module)

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
    print("Use Graphic Interface: (YES/NO)")
    if input() == "NO":
        USE_GRAPHIC_INTERFACE = False

    print("Environment Type: (HUMAN/AI)")
    if input() == "AI":
        ENVIRONMENT_TYPE = "AI"

    tf.app.run()
