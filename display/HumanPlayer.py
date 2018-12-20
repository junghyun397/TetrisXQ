import pygame as pygame
from pygame.rect import Rect

from agent.EnvironmentModel import EnvironmentModel

START_X = 20
START_Y = 20
BLOCK_SIZE = 20

COLOR_BACKGROUND = (38, 50, 56)
COLOR_DEF_BLOCK = (176, 190, 197)


class HumanPlayer(EnvironmentModel):

    def __init__(self, settings):
        super().__init__(settings)

        self._screen_width = settings['gridWidth'] * (BLOCK_SIZE + 2) + 300
        self._screen_height = settings['gridHeight'] * (BLOCK_SIZE + 2)

        pygame.init()
        pygame.display.set_caption("TetrisXQ User Interface")
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._screen.fill(COLOR_BACKGROUND)
        pygame.display.update()

    def action_and_reward(self, action):
        pass

    def get_key_action(self):
        while True:
            for key_event in pygame.event.get():
                if key_event.type == pygame.KEYDOWN:
                    if key_event.key == pygame.K_SPACE:
                        return 0
                    elif key_event.key == pygame.K_w:
                        return 1
                    elif key_event.key == pygame.K_d:
                        return 2
                    elif key_event.key == pygame.K_p:
                        return 3
                elif key_event.type == pygame.QUIT:
                    return -1

    def _draw_tetromino(self, x, y, shape):
        for nx in range(len(shape)):
            for ny in range(len(shape[0])):
                if shape[nx][ny] == 1:
                    self._draw_block(y + ny, x + nx, COLOR_DEF_BLOCK)

    def _draw_block(self, x, y, color):
        pygame.draw.rect(
            self._screen,
            color,
            Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
            0
        )
