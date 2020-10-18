from car_controller import CarController


if __name__ == '__main__':
    try:
        controller = CarController()
        controller.follow_waypoints()
    except InterruptedError as e:
        # Shutdown on ctrl+c or window closed
        print('Shutting down as per user request...')
