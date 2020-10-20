
class CarInfo:
    steer_left = -20
    steer_right = 20
    deg_per_sec = 5  # How fast the wheel can turn, specified in degrees

    max_v = 30 / 3.6
    min_v = -30 / 3.6

    reasonable_v = 15 / 3.6
    steering_v = 8 / 3.6

    @staticmethod
    def bound_v(v: float) -> float:
        return max(min(v, CarInfo.max_v), CarInfo.min_v)

    @staticmethod
    def bound_s(s: int) -> int:
        return max(min(s, CarInfo.steer_right), CarInfo.steer_left)
