from abc import ABCMeta, abstractmethod


class TetrominoInterface(metaclass=ABCMeta):

    def __init__(self):
        self._TETROMINO_PIECE = self._build_rotate()
        self._TETROMINO_ROTATE = [len(x) - 1 for x in self._TETROMINO_PIECE]

    @abstractmethod
    def build_tetromino(self):
        pass

    def _build_rotate(self):
        base_tetromino, rs = self.build_tetromino(), []
        for tetromino in base_tetromino:
            local_rs, prv = [tetromino], tetromino
            for _ in range(3):
                prv = [[prv[j][i] for j in range(len(prv))] for i in range(len(prv[0])-1, -1, -1)]
                if local_rs.count(prv) == 0:
                    local_rs.append(prv)
            rs.append(local_rs)
        return rs

    def get_tetromino(self, code, rotate):
        return self._TETROMINO_PIECE[code][rotate]

    def get_tetromino_size(self, code, rotated):
        return len(self._TETROMINO_PIECE[code][rotated][0]), len(self._TETROMINO_PIECE[code][rotated])

    def get_tetromino_all(self):
        return self._TETROMINO_PIECE

    def get_rotate_count(self, code):
        return self._TETROMINO_ROTATE[code]
