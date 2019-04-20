import random

from Settings import Settings
from environment.AutoPlayEnvironment import TetrisAIEnvironment
from environment.ManualEnvironment import ManualPlayer
from graphics.DummyGraphicModule import DummyGraphicModule
from graphics.GraphicModule import GraphicModule

settings = Settings()


def random_tetromino():
    return random.randrange(0, settings.ACTIONS)


USE_GRAPHIC_INTERFACE = True
ENVIRONMENT_TYPE = "AI"
TETROMINO_AGENT = random_tetromino

print("Use Graphic Interface: (YES/NO Enter=YES)")
if input().upper() == "NO":
    USE_GRAPHIC_INTERFACE = False

print("Environment Type: (HUMAN/AI Enter=AI)")
if input().upper() == "HUMAN":
    ENVIRONMENT_TYPE = "HUMAN"

graphic_module = DummyGraphicModule()
if USE_GRAPHIC_INTERFACE:
    graphic_module = GraphicModule(settings)
if ENVIRONMENT_TYPE == "HUMAN":
    env_model = ManualPlayer(settings, graphic_module)
else:
    env_model = TetrisAIEnvironment(settings, graphic_module)

turns = 0
while True:
    turns += 1
    _, _, end = env_model.action_and_reward(TETROMINO_AGENT())
    if end:
        print("Turns: " + str(turns))
        turns = 0
