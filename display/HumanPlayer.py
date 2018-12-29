import time

import pygame as pygame

from agent.EnvironmentModel import EnvironmentModel

FORCE_DOWN_TIME = 0.5
FORCE_SET_TIME = 1
KEY_CHAIN_TIME = 0.15


class HumanPlayer(EnvironmentModel):

    def __init__(self, settings, graphic_module):
        super().__init__(settings, graphic_module)

        self._board_height = settings.GRID_HEIGHT
        self._board_width = settings.GRID_WIDTH

        self._current_y = 0
        self._current_x = 0
        self._reset_pos()
        self._current_next = False

    def _reset_pos(self):
        self._current_y = 0
        self._current_x = round(self._board_width / 2) - round(len(self.tetris_model.current_tetromino[0]) / 2)

    def action_and_reward(self, action):
        self.tetris_model.next_state(action)

        self._reset_pos()
        self._current_next = True

        if self.graphic_module.tetris_model is None:
            self.graphic_module.set_tetris_model(self.tetris_model)
        self.graphic_module.draw_graphic(self._current_y, self._current_x)

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
                self.graphic_module.draw_graphic(self._current_y, self._current_x)
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
        self.graphic_module.draw_graphic(self._current_y, self._current_x)
        self.tetris_model.sum_tetromino(self._current_y, self._current_x)
        self._current_next = False

    def _move_tetromino(self, y, x):
        if self.tetris_model.can_move_block(self._current_y + y, self._current_x + x):
            self._current_y += y
            self._current_x += x
            self.graphic_module.draw_graphic(self._current_y, self._current_x)
            return True
        return False
