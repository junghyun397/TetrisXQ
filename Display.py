import argparse
import random

from Settings import Settings
from environment.AutoPlayEnvironment import AutoPlayEnvironment
from environment.ManualPlayEnvironment import ManualPlayer
from graphics.DummyGraphicModule import DummyGraphicModule
from graphics.GraphicModule import GraphicModule

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--env-type", help="Set environment type", type=str, default="auto")
parser.add_argument("-g", "--use-graphic", help="Using graphic interface", type=bool, default=True)
args = parser.parse_args()

settings = Settings()


def random_tetromino():
    return random.randrange(0, settings.ACTIONS)


TETROMINO_AGENT = random_tetromino

if __name__ == '__main__':
    settings = Settings()

    if args.use_graphic:
        graphic_interface = GraphicModule(settings)
    else:
        graphic_interface = DummyGraphicModule()

    if args.env_type == "manual":
        env_model = ManualPlayer(settings, graphic_interface)
    else:
        env_model = AutoPlayEnvironment(settings, graphic_interface)

    turns = 0
    while True:
        turns += 1
        _, _, end = env_model.action(TETROMINO_AGENT())
        if end:
            print("Turns: " + str(turns))
            turns = 0
