
class Settings:

    def __init__(self):
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10

        self.STATES = self.GRID_WIDTH * self.GRID_HEIGHT
        self.ACTIONS = 7
        self.HIDDEN_SIZE = 300

        self.DISCOUNT = 0.8
        self.LEARNING_LATE = 0.2

        self.BATCH_SIZE = 100
        self.MAX_MEMORY = 1000
