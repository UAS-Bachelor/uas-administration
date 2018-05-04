import argparse
import configparser
import sys
from os import system

import requests
from flask import Flask, render_template

app = Flask(__name__)

config = configparser.ConfigParser()
services = configparser.ConfigParser()
config.read('config.ini')
services.read('services.ini')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new-mission')
def new_mission():
    new_mission_request = get("pre_flight", "/new-mission")
    return render_template('layout.html', html=new_mission_request)


@app.route('/view-missions')
def view_missions():
    view_missions_service = get("post_flight", "/view-missions")
    return render_template('layout.html', html=view_missions_service)


@app.route('/view-mission/<id>')
def view_mission(id):
    view_mission_service = get("post_flight", "/view-mission/" + id)
    return render_template('layout.html', html=view_mission_service)


def get(service, route):
    try:
        url = config['Routing']['base_url'] + ":" + services[service]['port'] + route
        service_request = requests.get(url).text
        return service_request
    except requests.exceptions.ConnectionError:
        return service + " service unavailable"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5003,
                        help='specify which port to run this service on')
    parser.add_argument('-v', '--version', type=float, default=0,
                        help='specify which version of the service this is')
    args = parser.parse_args()
    args.prog = sys.argv[0].split('/')[-1].split('.')[0]

    print('Running {} service version {}'.format(args.prog, args.version))
    system('title {} service version {} on port {}'.format(
        args.prog, args.version, args.port))
    app.run(port=args.port, debug=True)
