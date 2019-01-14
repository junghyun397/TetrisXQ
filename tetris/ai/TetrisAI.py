from agent.EnvironmentModel import EnvironmentModel
from tetris.Tetromino import Tetromino

WEIGHT_FULL = 40
WEIGHT_FLAT = 2

WEIGHT_POST_SIDE = 2
WEIGHT_POST_FLOOR = 2

WEIGHT_HEIGHT = -1
WEIGHT_DEEP_HOLE = -3
WEIGHT_ROOF = -6


class TetrisAI(EnvironmentModel):

    def __init__(self, settings, graphic_module):
        super().__init__(settings, graphic_module)

    def do_action(self):
        max_score = -999999999
        chosen_state = None

        _, d_height, d_deep_hole, d_roof = self.tetris_model.analysis_board(self.tetris_model.board)

        states = self._get_state_list()
        for index in range(len(states)):
            board, _, _, _, post_side, post_floor = states[index]
            full, height, deep_hole, roof = self.tetris_model.analysis_board(board)

            score = 0

            score += full * WEIGHT_FULL
            score += post_side * WEIGHT_POST_SIDE
            score += post_floor * WEIGHT_POST_FLOOR

            score += (height - d_height) * WEIGHT_HEIGHT
            score += deep_hole * WEIGHT_DEEP_HOLE
            score += roof * WEIGHT_ROOF

            if height > self.board_height - 1:
                score = -999999999

            if score > max_score:
                max_score = score
                chosen_state = states[index]

        if chosen_state is None:
            self.tetris_model.is_end = True
            self.graphic_module.draw_graphic(-1, -1)
        else:
            b, y, x, rotate, _, _ = chosen_state
            self.tetris_model.rotate_block_rate(y, x, rotate)
            self.graphic_module.draw_graphic(y, x)
            self.tetris_model.sum_tetromino(y, x)

        self.graphic_module.pump_event()

    def _get_state_list(self):
        states = dict()

        num_index = 0
        rotate_count = Tetromino.get_rotate_count(self.tetris_model.current_shape_code) + 1
        for rotate_rate in range(rotate_count):
            for x in range(self.board_width):
                if self.tetris_model.rotate_block_rate(0, x, rotate_rate):
                    dy = 0
                    while self.tetris_model.can_move_block(dy + 1, x):
                        dy += 1

                    def check_pos(fy, fx):
                        if fy >= self.board_height or fx >= self.board_width or fx < 0 or self.tetris_model.get_board(fy, fx) == 1:
                            return True
                        return False

                    post_floor = 0
                    post_side = 0
                    for col in range(len(self.tetris_model.current_tetromino)):
                        for row in range(len(self.tetris_model.current_tetromino[0])):
                            if self.tetris_model.current_tetromino[col][row] == 1:
                                if check_pos(dy + col, x + row - 1):
                                    post_side += 1
                                if check_pos(dy + col, x + row + 1):
                                    post_side += 1
                                if check_pos(dy + col + 1, x + row):
                                    post_floor += 1

                    states[num_index] = self.tetris_model.get_sum_tetromino_board(dy, x), dy, x, rotate_rate, post_side, post_floor
                    num_index += 1
        return states
