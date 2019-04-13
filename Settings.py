from environment.RewardType import RewardType


class Settings:

    def __init__(self):
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10

        self.LEARNING_EPOCH = 2000
        self.MAX_TURNS = 100000

        self.START_EPSILON = 1
        self.MIN_EPSILON = 0.01

        self.STATES = self.GRID_WIDTH * self.GRID_HEIGHT
        self.ACTIONS = 7
        self.HIDDEN_SIZE = 300

        self.DISCOUNT = 0.8
        self.LEARNING_LATE = 0.2

        self.BATCH_SIZE = 100
        self.MAX_MEMORY = 1000

        self.REWARD_MODE = RewardType.BY_SUM_TURNS
