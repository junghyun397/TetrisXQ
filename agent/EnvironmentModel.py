from abc import ABCMeta


class EnvironmentModel(metaclass=ABCMeta):

    def action_and_reward(self, action):
        """
        환경에 대한 행동 이후 보상을 얻어옴
        :param action: int, 0~8의 Action 값
        :return state: np.ndarray, 행동 이후 환경 반환
                 reward: float, 0~1 점수 반환
                 isEnd: boolean, 종료 여부 반환
        """
        pass

    def get_state(self):
        """
        현재 환경을 반환함
        :return: state: np.ndarray, 환경 반환
        """
        pass
