
class CarInfo:
    steer_left = -20
    steer_right = 20

    max_v = 100
    min_v = -100

    @staticmethod
    def bound_v(v: int) -> int:
        return max(min(v, CarInfo.max_v), CarInfo.min_v)

    @staticmethod
    def bound_s(s: int) -> int:
        return max(min(s, CarInfo.steer_right), CarInfo.steer_left)
