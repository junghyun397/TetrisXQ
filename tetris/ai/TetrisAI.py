import numpy as np

from agent.EnvironmentModel import EnvironmentModel
from tetris.Tetromino import Tetromino

WEIGHT_FULL = 1000
WEIGHT_WALL = 2
WEIGHT_FLAT = 1

WEIGHT_HEIGHT = -50
WEIGHT_HOLE = -1
WEIGHT_DEEP_HOLE = -5
WEIGHT_APERTURE = -8

USE_MAX = True


class TetrisAI(EnvironmentModel):

    def __init__(self, settings, graphic_module):
        super().__init__(settings, graphic_module)

        self._def_height = 0
        self._def_walls = 0
        self._def_flat = 0

        self._def_holes = 0
        self._def_deep_holes = 0
        self._def_apertures = 0

        self._def_x = round(self.board_width / 2) - round(len(self.tetris_model.current_tetromino[0]) / 2)

    def do_action(self):
        states = self._get_state_list()
        chosen_state = None
        max_score = -1000

        _, self._def_walls, self._def_flat, self._def_height, self._def_holes, self._def_deep_holes, self._def_apertures \
            = self._get_scores(self.tetris_model.get_board_data())

        for index in range(len(states)):
            fulls, wall_sum, flat_sum, height, holes, deep_holes, apertures = self._get_scores(states[index])

            state_score = -1
            state_score += fulls * WEIGHT_FULL

            if USE_MAX:
                state_score += max(wall_sum - self._def_walls, 0) * WEIGHT_WALL
                state_score += max(flat_sum - self._def_flat, 0) * WEIGHT_FLAT

                state_score += max(height - self._def_height, 0) * WEIGHT_HEIGHT
                state_score += max(holes - self._def_holes, 0) * WEIGHT_HOLE
                state_score += max(deep_holes - self._def_deep_holes, 0) * WEIGHT_DEEP_HOLE
                state_score += max(apertures - self._def_apertures, 0) * WEIGHT_APERTURE
            else:
                state_score += (wall_sum - self._def_walls) * WEIGHT_WALL
                state_score += (flat_sum - self._def_flat) * WEIGHT_FLAT

                state_score += (height - self._def_height) * WEIGHT_HEIGHT
                state_score += (holes - self._def_holes) * WEIGHT_HOLE
                state_score += (deep_holes - self._def_deep_holes) * WEIGHT_DEEP_HOLE
                state_score += (apertures - self._def_apertures) * WEIGHT_APERTURE

            if state_score > max_score:
                max_score = state_score
                chosen_state = states[index]

        # print(self._get_scores(chosen_state))

        if len(states) == 0:
            self.tetris_model.is_end = True
        else:
            self.tetris_model.board = chosen_state
        self.tetris_model.update_board()

        self.graphic_module.draw_graphic(-1, -1)
        self.graphic_module.pump_event()

    def _get_state_list(self):
        states = dict()
        index = 0
        for x in range(self.board_width):
            for rotate in range(Tetromino.get_rotate_count(self.tetris_model.current_shape_code) + 1):
                if self.tetris_model.rotate_block_rate(0, x, rotate):
                    n_states = self.tetris_model.get_board_data()
                    cov_y = 0
                    while self.tetris_model.can_move_block(cov_y + 1, x):
                        cov_y += 1
                    for col in range(len(self.tetris_model.current_tetromino)):
                        for row in range(len(self.tetris_model.current_tetromino[0])):
                            if self.tetris_model.get_board(cov_y + col, x + row) == 0 \
                                    and self.tetris_model.current_tetromino[col][row] == 1:
                                n_states[(cov_y + col) * self.board_width + x + row] = 1
                    states[index] = n_states
                    index += 1
        return states

    def _get_scores(self, state):
        fulls = 0
        wall_sum = 0
        flat_sum = 0

        height = 0
        holes = 0
        deep_holes = 0
        apertures = 0

        sides = self.tetris_model.get_clear_board()

        for y in range(self.board_height):
            line_sum = np.sum(state[y * self.board_width:(y + 1) * self.board_width])
            wall_sum += state[y * self.board_width] + state[y * self.board_width + self.board_width - 1]
            if line_sum == self.board_width:
                fulls += 1
            elif line_sum > 0:
                height += 1

            chain_x = False
            for x in range(self.board_width):
                d_hole = 0
                sum_side = 0
                if x is not 0:
                    sum_side += state[y * self.board_width + x - 1]
                    d_hole += state[y * self.board_width + x - 1]
                else:
                    sum_side += 1
                if x is not self.board_width - 1:
                    sum_side += state[y * self.board_width + x + 1]
                    d_hole += state[y * self.board_width + x + 1]
                    if state[y * self.board_width + x] + state[y * self.board_width + x + 1] == 2:
                        if chain_x:
                            flat_sum += 1
                        else:
                            chain_x = True
                else:
                    sum_side += 1
                sides[y * self.board_width + x] = sum_side
                if sum_side > 0:
                    holes += 1

        for x_index in range(self.board_width):
            has_deep_hole = False
            for y_index in range(self.board_height):
                dy_index = self.board_height - y_index - 1
                if dy_index < self.board_height - 3:
                    if sides[dy_index * self.board_width + x_index] \
                            + sides[(dy_index + 1) * self.board_width + x_index] \
                            + sides[(dy_index + 2) * self.board_width + x_index] == 6 and state[
                        dy_index * self.board_width + x_index] + state[(dy_index + 1) * self.board_width + x_index] + \
                            state[(dy_index + 2) * self.board_width + x_index] == 0 and not has_deep_hole:
                        deep_holes += 1
                        has_deep_hole = True
                if dy_index < self.board_height - 1:
                    if state[dy_index * self.board_width + x_index] == 0 and state[(dy_index + 1) * self.board_width + x_index] == 1:
                        ddy_index = 0
                        while state[(dy_index + ddy_index) * self.board_width + x_index] == 0 and dy_index + ddy_index < self.board_height - 1:
                            ddy_index += 1
                            apertures += ddy_index

        return fulls, wall_sum, flat_sum, height, holes, deep_holes, apertures
