from tetris.ClassicTetromino import ClassicTetromino


class Settings:

    def __init__(self, grid_height=22,
                 grid_width=10,
                 tetromino=ClassicTetromino()):
        self.GRID_HEIGHT = grid_height
        self.GRID_WIDTH = grid_width

        self.TETROMINO = tetromino

        self.STATES = self.GRID_WIDTH * self.GRID_HEIGHT
        self.ACTIONS = len(tetromino.get_tetromino_all())
