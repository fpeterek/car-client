from typing import Optional, List
import json
import os

from flask import Flask, request

from car_controller import CarController
from waypoint import Waypoint


controller: Optional[CarController] = None

app = Flask('CarApi')
app.debug = False


def init(car: CarController) -> None:
    global controller
    controller = car
    global app

    app.run(port=int(os.environ['API_PORT']))


def position_object():
    pos = controller.pt.current_position
    return {
        'latitude': pos[1],
        'longitude': pos[0]
    }


def heading():
    return controller.pt.rotation


def waypoints_list() -> List[dict]:
    waypoints = controller.get_waypoints()
    return [wp.dict for wp in waypoints]


def get_waypoints():
    return json.dumps(waypoints_list())


def post_waypoint() -> str:
    post = request.get_json() if request.is_json else json.loads(request.get_data())
    lat = post['latitude']
    lon = post['longitude']
    controller.add_waypoint(Waypoint(x=lon, y=lat))
    return '{"status": "success"}'


def delete_waypoint() -> str:
    wp_id = request.args.get('id')
    if wp_id is not None and str(wp_id).isnumeric():
        controller.remove_waypoint(int(wp_id))
        return '{"status": "success"}'
    return '{"status": "failure"}'


@app.route('/waypoints', methods=['GET', 'POST', 'DELETE'])
def waypoints_route():
    if request.method == 'GET':
        return get_waypoints()
    if request.method == 'POST':
        return post_waypoint()
    if request.method == 'DELETE':
        return delete_waypoint()


@app.route('/info', methods=['GET'])
def get_info() -> str:
    pos = position_object()
    head = heading()
    waypoints = waypoints_list()
    info = {
        'position': pos,
        'heading': head,
        'waypoints': waypoints
    }
    return json.dumps(info)


@app.route('/position', methods=['GET'])
def get_position() -> str:
    return json.dumps(position_object())


@app.route('/heading', methods=['GET'])
def get_heading() -> str:
    dct = {
        'heading': heading()
    }
    return json.dumps(dct)
