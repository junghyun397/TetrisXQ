class Settings:

    def __init__(self, grid_height=22,
                 grid_width=10,
                 actions=7,
                 hidden_size=300,
                 discount=0.8,
                 learning_rate=0.2):
        self.GRID_HEIGHT = grid_height
        self.GRID_WIDTH = grid_width

        self.STATES = self.GRID_WIDTH * self.GRID_HEIGHT
        self.ACTIONS = actions
        self.HIDDEN_SIZE = hidden_size

        self.DISCOUNT = discount
        self.LEARNING_LATE = learning_rate
