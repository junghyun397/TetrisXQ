import numpy
import pygame as pygame
from pygame.rect import Rect

from agent.EnvironmentModel import EnvironmentModel
from tetris.Tetromino import Tetromino

START_X = 20
START_Y = 20
BLOCK_SIZE = 20

COLOR_WHITE = (224, 224, 224)
COLOR_BLACK = (0, 0, 0)

COLOR_BACKGROUND = (38, 50, 56)

COLOR_BLOCK = [(176, 190, 197), (176, 190, 197), (176, 190, 197), (176, 190, 197), (176, 190, 197), (176, 190, 197)]


class HumanPlayer(EnvironmentModel):

    def __init__(self, settings):
        super().__init__(settings)

        self._board_width = settings.GRID_WIDTH
        self._board_height = settings.GRID_HEIGHT
        self._screen_width = self._board_width * (BLOCK_SIZE + 2) + 300
        self._screen_height = self._board_height * (BLOCK_SIZE + 2)

        self._interface_board = numpy.zeros((self._board_width, self._board_height))

        pygame.init()
        pygame.display.set_caption("TetrisXQ User Interface")
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._screen.fill(COLOR_BACKGROUND)
        pygame.display.update()

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)
        while True:
            break
        return self.get_vector_state(), self.get_reward(), self.tetris_model.is_end

    def on_key_press(self, key_type):
        if key_type == pygame.K_w:
            return 0
        elif key_type == pygame.K_a:
            return 1
        elif key_type == pygame.K_s:
            return 2
        elif key_type == pygame.K_d:
            return 3
        elif key_type == pygame.K_SPACE:
            return 4

    def _draw_tetromino(self, x, y, shape):
        for i in range(len(shape)):
            for o in range(len(shape[0])):
                if shape[i][o] != 0:
                    self._interface_board[x + o][y + i] = 1

    def _update_screen(self):
        for x in range(self._board_width):
            for y in range(self._board_height):
                if self._interface_board[x][y] != 0:
                    self._draw_block(x, y, self._interface_board[x][y])
        pygame.display.update()

    def _draw_block(self, x, y, color):
        pygame.draw.rect(
            self._screen,
            color,
            Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            0
        )
