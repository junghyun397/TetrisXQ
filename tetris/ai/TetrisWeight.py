class TetrisWeight:

    def __init__(self, weight_full=5,
                 weight_flat=2,
                 weight_post_side=2,
                 weight_post_floor=2,
                 weight_height=-1,
                 weight_deep_hole=-3,
                 weight_roof=-10):
        self.WEIGHT_FULL = weight_full
        self.WEIGHT_FLAT = weight_flat

        self.WEIGHT_POST_SIDE = weight_post_side
        self.WEIGHT_POST_FLOOR = weight_post_floor

        self.WEIGHT_HEIGHT = weight_height
        self.WEIGHT_DEEP_HOLE = weight_deep_hole
        self.WEIGHT_ROOF = weight_roof
