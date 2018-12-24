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

        self._current_x = 0
        self._current_y = 0

        self._board_width = settings.GRID_WIDTH
        self._board_height = settings.GRID_HEIGHT
        self._screen_width = self._board_width * (BLOCK_SIZE + 2) + 300
        self._screen_height = self._board_height * (BLOCK_SIZE + 2)

        self._interface_board = numpy.zeros((self._board_height, self._board_width))

        pygame.init()
        pygame.display.set_caption("TetrisXQ User Interface")
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._screen.fill(COLOR_BACKGROUND)
        pygame.display.update()

        # TODO: DEBUG -------------------------------------------
        self._draw_tetromino(0, 1, Tetromino.get_tetromino(3, 2))
        self._update_screen()
        print(self._interface_board)
        # -------------------------------------------------------

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)
        is_set = False
        while is_set:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.on_key_press(event.key)
        return self.get_vector_state(), self.get_reward(), self.tetris_model.is_end

    def on_key_press(self, key):
        if key == pygame.K_w:
            self.tetris_model.rotate_block(self._current_y, self._current_x)
        elif key == pygame.K_a:
            pass
        elif key == pygame.K_s:
            pass
        elif key == pygame.K_d:
            pass
        elif key == pygame.K_SPACE:
            pass

    def _draw_tetromino(self, y, x, shape):
        for i in range(len(shape)):
            for o in range(len(shape[0])):
                if shape[i][o] != 0:
                    self._interface_board[y + i][x + o] = 1

    def _update_screen(self):
        for y in range(self._board_height):
            for x in range(self._board_width):
                if self._interface_board[y][x] != 0:
                    self._draw_block(y, x, COLOR_WHITE)
        pygame.display.update()

    def _draw_block(self, y, x, color):
        pygame.draw.rect(
            self._screen,
            color,
            Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            0
        )
