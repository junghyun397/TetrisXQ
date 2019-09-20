from abc import ABCMeta, abstractmethod


class TetrominoInterface(metaclass=ABCMeta):

    @abstractmethod
    def get_tetromino(self, code, rotate):
        pass

    @abstractmethod
    def get_tetromino_size(self, code, rotated):
        pass

    @abstractmethod
    def get_tetromino_all(self):
        pass

    @abstractmethod
    def get_rotate_count(self, code):
        pass
