from graphics.GraphicInterface import GraphicInterface


class DummyGraphicModule(GraphicInterface):

    def draw_graphic(self, tetromino_y, tetromino_x):
        pass

    def set_tetris_model(self, tetris_model):
        pass

    def pump_event(self):
        pass
