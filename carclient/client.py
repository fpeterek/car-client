import socket
import os

from car_info import CarInfo

host = os.getenv("SERVER_HOST")
port = int(os.getenv("SERVER_PORT"))


def to_bytes(value: int) -> bytes:
    return value.to_bytes(1, 'little', signed=True)


def send_data(velocity: int, steering_angle: int) -> None:

    velocity = CarInfo.bound_v(velocity)
    steering_angle = CarInfo.bound_s(steering_angle)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(to_bytes(velocity) + to_bytes(steering_angle))
        if not int(sock.recv(1)[0]):
            raise Exception('Message rejected by car')


def read_v():
    return CarInfo.bound_v(int(input('New velocity: ')))


def read_s():
    return CarInfo.bound_s(int(input('New steering angle: ')))


def menu():

    v = 0
    s = 0

    while True:
        print('[a] Set Velocity  [b] Set Steering Angle  [c] Print Current')
        i = input('> ')
        if i == 'a':
            v = read_v()
        if i == 'b':
            s = read_s()
        if i in ('a', 'b'):
            send_data(v, s)

        if i == 'c':
            print(f'Current (velocity, angle) = ({v}, {s})')
