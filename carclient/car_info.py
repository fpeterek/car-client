
class CarInfo:
    steer_left = -20
    steer_right = 20

    max_v = 30 / 3.6
    min_v = -30 / 3.6

    @staticmethod
    @property
    def reasonable_v() -> float:
        return 10 / 3.6

    @staticmethod
    def bound_v(v: float) -> float:
        return max(min(v, CarInfo.max_v), CarInfo.min_v)

    @staticmethod
    def bound_s(s: int) -> int:
        return max(min(s, CarInfo.steer_right), CarInfo.steer_left)
