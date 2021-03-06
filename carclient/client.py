import socket
import os
from typing import Tuple

from car_info import CarInfo

_host = os.getenv("SERVER_HOST")
_port = int(os.getenv("SERVER_PORT"))
_camera = os.getenv('CAMERA_HOST')
_camera_port = int(os.getenv('CAMERA_PORT'))


def _to_bytes(value: int, signed: bool = True) -> bytes:
    return value.to_bytes(1, 'little', signed=signed)


_padding = _to_bytes(0)


class _MessageType:
    drive = _to_bytes(0, signed=False)
    healthcheck = _to_bytes(1, signed=False)
    info = _to_bytes(2, signed=False)
    ebrake = _to_bytes(3, signed=False)
    position = _to_bytes(4, signed=False)


def drive(velocity: int, steering_angle: int) -> bool:

    velocity = CarInfo.bound_v(velocity)
    steering_angle = CarInfo.bound_s(steering_angle)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.drive + _to_bytes(int(velocity * 10)) + _to_bytes(steering_angle))

        return bool(sock.recv(1)[0])


def healthcheck() -> bool:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.healthcheck + _padding + _padding)

        return bool(sock.recv(1)[0])


def info() -> Tuple[float, int, bool]:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.info + _padding + _padding)

        data = sock.recv(3)

        v = int.from_bytes(data[0:1], 'little', signed=True) / 10
        s = int.from_bytes(data[1:2], 'little', signed=True)
        b = bool(int.from_bytes(data[2:3], 'little', signed=True))

        return v, s, b


def position() -> Tuple[float, float]:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.position + _padding + _padding)

        data = sock.recv(17)

        ok = bool(int.from_bytes(data[0:1], 'little', signed=False))
        x = int.from_bytes(data[1:9], 'little', signed=True) / 10_000_000_000
        y = int.from_bytes(data[9:], 'little', signed=True) / 10_000_000_000

        return (y, x) if ok else None


def ebrake(val: bool) -> bool:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_host, _port))
        sock.sendall(_MessageType.ebrake + _to_bytes(int(val)) + _padding)

        return bool(sock.recv(1)[0])


def camera_info() -> Tuple[float, float]:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((_camera, _camera_port))

        split = sock.recv(13).decode('utf-8').split(' ')
        s = float(split[0]) / 100
        sign = int(split[2])
        c = int(split[1]) / 100 * (1, -1)[sign]

        return s, c
