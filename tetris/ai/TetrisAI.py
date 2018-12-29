from agent.EnvironmentModel import EnvironmentModel


class TetrisAI(EnvironmentModel):

    def __init__(self, settings, graphic_module):
        super().__init__(settings, graphic_module)

    def action_and_reward(self, action):
        return super().get_current_state(), 1.0, False  # TODO: REMOVE IT (TEMP)
