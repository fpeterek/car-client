from client import drive, healthcheck, info
from car_info import CarInfo


def read_v():
    return CarInfo.bound_v(int(input('New velocity: ')))


def read_s():
    return CarInfo.bound_s(int(input('New steering angle: ')))


def menu():

    v = 0
    s = 0

    while True:
        print('[a] Set Velocity  [b] Set Steering Angle  [c] Print Current  [d] Healthcheck')
        i = input('> ')
        if i == 'a':
            v = read_v()
        if i == 'b':
            s = read_s()
        if i in ('a', 'b'):
            drive(v, s)

        if i == 'c':
            cv, cs = info()
            print(f'Current (velocity, angle) = ({cv}, {cs})')

        if i == 'd':
            print(['Dead', 'Alive'][healthcheck()])
