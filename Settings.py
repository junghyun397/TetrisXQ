
class Settings:

    def __init__(self):
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 22

        self.RAND_SEED = 503
        self.LEARNING_EPOCH = 2000

        self.STATES = self.GRID_WIDTH * self.GRID_HEIGHT
        self.ACTIONS = 7
        self.HIDDEN_SIZE = 100

        self.DISCOUNT = 0.9
        self.LEARNING_LATE = 0.001

        self.BATCH_SIZE = 50
        self.MAX_MEMORY = 100
