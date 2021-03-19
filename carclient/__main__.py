from threading import Thread

from car_controller import CarController
import api


if __name__ == '__main__':
    try:
        controller = CarController()
        thread: Thread = Thread(target=lambda: api.init(controller))
        thread.setDaemon(True)
        thread.start()
        controller.follow_waypoints()
    except InterruptedError as e:
        # Shutdown on ctrl+c or window closed
        print('Shutting down as per user request...')
        exit(0)
