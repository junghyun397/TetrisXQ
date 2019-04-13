import random

from Settings import Settings
from TrainDQN import TrainInfo
from environment.player.HumanPlayer import HumanPlayer
from environment.player.TetrisAIPlayer import TetrisAIPlayer
from graphics.DummyGraphicModule import DummyGraphicModule
from graphics.GraphicModule import GraphicModule
from tetris.ai.TetrisAI import TetrisAI

settings = Settings()
train_info = TrainInfo(settings)


def random_tetromino():
    return random.randrange(0, settings.ACTIONS)


def build_ai_tetromino_agent(env):
    agent = TetrisAI(settings, env.tetris_model)

    def agent_func():
        _, chosen_score = agent.get_evaluated_states()
        return chosen_score

    return agent_func


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
    graphic_module = GraphicModule(settings, train_info)
if ENVIRONMENT_TYPE == "HUMAN":
    env_model = HumanPlayer(settings, graphic_module)
else:
    env_model = TetrisAIPlayer(settings, graphic_module)

print("Tetromino Agent Type: (RANDOM/AI Enter=RANDOM)")
if input().upper() == "AI":
    TETROMINO_AGENT = build_ai_tetromino_agent(env_model)

turns = 0
while True:
    turns += 1
    _, _, end = env_model.action_and_reward(TETROMINO_AGENT())
    if end:
        train_info.current_epoch += 1
        print("Turns: " + str(turns))
        turns = 0
