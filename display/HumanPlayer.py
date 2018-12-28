import time

import numpy as np
import pygame as pygame
from pygame.rect import Rect

from agent.EnvironmentModel import EnvironmentModel

FORCE_DOWN_TIME = 0.5
FORCE_SET_TIME = 1
KEY_CHAIN_TIME = 0.15

BLOCK_SIZE = 30
LINE_SIZE = round(BLOCK_SIZE / 10)

COLOR_BACKGROUND = (240, 240, 240)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (189, 189, 189)
COLOR_BLACK = (0, 0, 0)
COLOR_BLOCK = [(176, 190, 197), (183, 28, 28), (74, 20, 140), (26, 35, 126), (130, 119, 23), (27, 94, 32),
               (191, 54, 12), (62, 39, 35)]


class HumanPlayer(EnvironmentModel):

    def __init__(self, settings, train_info):
        super().__init__(settings)

        self.train_info = train_info

        self._board_height = settings.GRID_HEIGHT
        self._board_width = settings.GRID_WIDTH
        self._screen_width = (self._board_width + 2) * BLOCK_SIZE + 300
        self._screen_height = (self._board_height + 2) * BLOCK_SIZE

        self._current_y = 0
        self._current_x = 0
        self._reset_pos()
        self._current_next = False

        self._interface_board = np.zeros((self._board_height, self._board_width))

        pygame.init()
        pygame.display.set_caption("TetrisXQ User Interface")
        self._font_obj = pygame.font.SysFont('Arial', BLOCK_SIZE)
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self._screen.fill(COLOR_BACKGROUND)
        pygame.draw.rect(self._screen, COLOR_BLACK,
                         Rect(BLOCK_SIZE - LINE_SIZE, BLOCK_SIZE - LINE_SIZE,
                              self._board_width * BLOCK_SIZE + LINE_SIZE * 2,
                              self._board_height * BLOCK_SIZE + LINE_SIZE * 2),
                         0)
        pygame.display.update()

    def _reset_pos(self):
        self._current_y = 0
        self._current_x = round(self._board_width / 2) - round(len(self.tetris_model.current_tetromino[0]) / 2)

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)

        self._reset_pos()
        self._current_next = True

        self._update_screen()

        current_tet_time = time.time()
        current_key_time = time.time()
        while self._current_next:
            if time.time() - current_tet_time > FORCE_DOWN_TIME:
                if not self._move_tetromino(1, 0):
                    pass
                current_tet_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self._on_key_press(event.key)
                    current_key_time = time.time()
                elif event.type == pygame.QUIT:
                    exit()
            if time.time() - current_key_time > KEY_CHAIN_TIME:
                if pygame.key.get_pressed()[pygame.K_a]:
                    self._on_key_press(pygame.K_a)
                elif pygame.key.get_pressed()[pygame.K_s]:
                    self._on_key_press(pygame.K_s)
                elif pygame.key.get_pressed()[pygame.K_d]:
                    self._on_key_press(pygame.K_d)
                current_key_time = time.time()

        return self.get_current_state(), self.get_reward(), self.tetris_model.is_end

    def _on_key_press(self, key):
        if key == pygame.K_w:
            if self.tetris_model.rotate_block(self._current_y, self._current_x):
                self._update_screen()
        elif key == pygame.K_a:
            self._move_tetromino(0, -1)
        elif key == pygame.K_s:
            if not self._move_tetromino(1, 0):
                self._set_tetromino()
        elif key == pygame.K_d:
            self._move_tetromino(0, 1)
        elif key == pygame.K_SPACE:
            while self.tetris_model.can_move_block(self._current_y + 1, self._current_x):
                self._current_y += 1
            self._set_tetromino()
        elif key == pygame.K_ESCAPE:
            resume = True
            while resume:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        resume = False

    def _set_tetromino(self):
        self._update_screen()
        self.tetris_model.sum_tetromino(self._current_y, self._current_x)
        self._current_next = False

    def _move_tetromino(self, y, x):
        if self.tetris_model.can_move_block(self._current_y + y, self._current_x + x):
            self._current_y += y
            self._current_x += x
            self._update_screen()
            return True
        return False

    def _update_screen(self):
        pygame.draw.rect(self._screen, COLOR_BACKGROUND,
                         Rect(BLOCK_SIZE, BLOCK_SIZE, self._board_width * BLOCK_SIZE, self._board_height * BLOCK_SIZE),
                         0)

        pygame.draw.rect(self._screen, COLOR_BACKGROUND,
                         Rect(self._screen_width - 300, BLOCK_SIZE, self._screen_width, self._screen_height),
                         0)

        self._draw_score_info()
        self._draw_train_info()

        self._interface_board = np.reshape(self.tetris_model.get_board_data(), (self._board_height, self._board_width))
        self._draw_tetromino()
        self._draw_ghost_tetromino()
        for y in range(self._board_height):
            for x in range(self._board_width):
                if self._interface_board[y][x] != 0:
                    self._draw_block(y, x, COLOR_BLOCK[self._interface_board[y][x] - 1])
        pygame.display.update()

    # PyGame UI

    def _draw_score_info(self):
        text_obj = self._font_obj.render("Score: " + str(round(self.tetris_model.score)), True, COLOR_BLACK)
        self._screen.blit(text_obj, (self._screen_width - 300, BLOCK_SIZE))

    def _draw_train_info(self):
        if self.train_info is not None:
            text_obj = self._font_obj.render("Epoch: " + str(self.train_info.current_epoch) +
                                             "/" + str(self.train_info.total_epoch), True, COLOR_BLACK)
            self._screen.blit(text_obj, (self._screen_width - 300, BLOCK_SIZE * 3))

    # PyGame Draw

    def _draw_tetromino(self):
        for col in range(len(self.tetris_model.current_tetromino)):
            for row in range(len(self.tetris_model.current_tetromino[0])):
                if self._interface_board[self._current_y + col][self._current_x + row] == 0 \
                        and self.tetris_model.current_tetromino[col][row] == 1:
                    self._interface_board[self._current_y + col][self._current_x + row] \
                        = self.tetris_model.current_shape_code + 2

    def _draw_ghost_tetromino(self):
        temp_y = 0
        while self.tetris_model.can_move_block(temp_y + 1, self._current_x):
            temp_y += 1
        for col in range(len(self.tetris_model.current_tetromino)):
            for row in range(len(self.tetris_model.current_tetromino[0])):
                if self.tetris_model.current_tetromino[col][row] == 1:
                    self._draw_ghost_block(temp_y + col, self._current_x + row)

    def _draw_block(self, y, x, color):
        pygame.draw.rect(self._screen, color,
                         Rect((x + 1) * BLOCK_SIZE + LINE_SIZE / 2, (y + 1) * BLOCK_SIZE + LINE_SIZE / 2,
                              BLOCK_SIZE - LINE_SIZE / 2, BLOCK_SIZE - LINE_SIZE / 2),
                         0)
        pygame.draw.rect(self._screen, COLOR_BLACK,
                         Rect((x + 1) * BLOCK_SIZE + LINE_SIZE / 2, (y + 1) * BLOCK_SIZE + LINE_SIZE / 2,
                              BLOCK_SIZE - LINE_SIZE / 2, BLOCK_SIZE - LINE_SIZE / 2),
                         LINE_SIZE)

    def _draw_ghost_block(self, y, x):
        pygame.draw.rect(self._screen, COLOR_GRAY,
                         Rect((x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                         0)
