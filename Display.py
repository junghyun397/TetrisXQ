import random

from Settings import Settings
from Train import TrainInfo
from display.DummyGraphicModule import DummyGraphicModule
from display.GraphicModule import GraphicModule
from display.HumanPlayer import HumanPlayer
from tetris.ai.TetrisAI import TetrisAI

USE_GRAPHIC_INTERFACE = True
ENVIRONMENT_TYPE = "AI"

print("Use Graphic Interface: (YES/NO Enter=YES)")
if input().upper() == "NO":
    USE_GRAPHIC_INTERFACE = False

print("Environment Type: (HUMAN/AI Enter=AI)")
if input().upper() == "HUMAN":
    ENVIRONMENT_TYPE = "HUMAN"

settings = Settings()
train_info = TrainInfo(settings)

graphic_module = DummyGraphicModule()
if USE_GRAPHIC_INTERFACE:
    graphic_module = GraphicModule(settings, train_info)
if ENVIRONMENT_TYPE == "HUMAN":
    env_model = HumanPlayer(settings, graphic_module)
else:
    env_model = TetrisAI(settings, graphic_module)

turns = 0
while True:
    turns += 1
    _, _, end = env_model.action_and_reward(random.randrange(0, settings.ACTIONS))
    if end:
        train_info.current_epoch += 1
        print("Turns: " + str(turns))
        turns = 0
