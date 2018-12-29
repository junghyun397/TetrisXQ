import random

from Settings import Settings
from Train import TrainInfo
from display.GraphicModule import GraphicModule
from display.HumanPlayer import HumanPlayer

settings = Settings()
train_info = TrainInfo(settings)

graphic_module = GraphicModule(settings, train_info)
env_model = HumanPlayer(settings, graphic_module)

while True:
    _, _, end = env_model.action_and_reward(random.randrange(0, settings.ACTIONS))
    if end:
        train_info.current_epoch += 1
