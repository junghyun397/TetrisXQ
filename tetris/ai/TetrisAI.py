from agent.EnvironmentModel import EnvironmentModel


class TetrisAI(EnvironmentModel):

    def __init__(self, settings):
        super().__init__(settings)

    def action_and_reward(self, action):
        return super().get_vector_state(), 1.0, False  # TODO: REMOVE IT (TEMP)
