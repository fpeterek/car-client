import socket
import os
from typing import Tuple

from car_info import CarInfo

_host = os.getenv("SERVER_HOST")
_port = int(os.getenv("SERVER_PORT"))


def _to_bytes(value: int, signed: bool = True) -> bytes:
    return value.to_bytes(1, 'little', signed=signed)


_padding = _to_bytes(0)


class _MessageType:
    drive = _to_bytes(0, signed=False)
    healthcheck = _to_bytes(1, signed=False)
    info = _to_bytes(2, signed=False)


def drive(velocity: int, steering_angle: int) -> bool:

    velocity = CarInfo.bound_v(velocity)
    steering_angle = CarInfo.bound_s(steering_angle)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.drive + _to_bytes(velocity) + _to_bytes(steering_angle))

        return bool(sock.recv(1)[0])


def healthcheck() -> bool:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.healthcheck + _padding + _padding)

        return bool(sock.recv(1)[0])


def info() -> Tuple[int, int]:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.info + _padding + _padding)

        data = sock.recv(2)

        v = int.from_bytes(data[0:1], 'little', signed=True)
        s = int.from_bytes(data[1:2], 'little', signed=True)

        return v, s
