from abc import ABCMeta, abstractmethod


class GraphicInterface(metaclass=ABCMeta):

    @abstractmethod
    def set_tetris_model(self, tetris_model):
        pass

    @abstractmethod
    def draw_graphic(self, tetromino_y, tetromino_x):
        pass
