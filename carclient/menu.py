from client import drive, healthcheck, info, ebrake
from car_info import CarInfo


def read_v():
    return CarInfo.bound_v(int(input('New velocity: ')))


def read_s():
    return CarInfo.bound_s(int(input('New steering angle: ')))


def read_ebrake():
    i = input('Emergency brake (1/0): ')
    return bool(int(i))


def menu():

    v = 0
    s = 0

    while True:
        print('[a] Set Velocity  [b] Set Steering Angle  [c] Print Current  [d] Healthcheck  [e] Emergency Brake')
        i = input('> ')
        if i == 'a':
            v = read_v()
        if i == 'b':
            s = read_s()
        if i in ('a', 'b'):
            drive(v, s)

        if i == 'c':
            cv, cs, eb = info()
            print(f'Current (velocity, angle) = ({cv}, {cs})')

        if i == 'd':
            print(['Dead', 'Alive'][healthcheck()])

        if i == 'e':
            ebrake(read_ebrake())

