import random

from Settings import Settings
from Train import TrainInfo
from agent.model.QMLPModel import QMLPModel
from display.HumanPlayer import HumanPlayer

settings = Settings()
train_info = TrainInfo()
train_info.total_epoch = settings.LEARNING_EPOCH

q_network_model = QMLPModel(settings)
env_model = HumanPlayer(settings, train_info)

while True:
    _, _, end = env_model.action_and_reward(random.randrange(0, settings.ACTIONS))
    if end:
        train_info.current_epoch += 1
