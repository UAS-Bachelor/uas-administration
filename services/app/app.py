import argparse
import sys
import configparser
from os import system

import requests
from flask import Flask, render_template

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    try:
        login = requests.get(config['Routing']['base_url'] + ':5002/login').text
    except requests.exceptions.ConnectionError:
        login = 'Login service unavailable'
    return render_template('layout.html', html=login)


@app.route('/new-mission')
def new_mission():
    try:
        new_mission_request = requests.get(config['Routing']['base_url'] + ':5004/new-mission').text
    except requests.exceptions.ConnectionError:
        return 'New Mission service unavailable'
    return render_template('layout.html', html=new_mission_request)


@app.route('/view-missions')
def view_missions():
    try:
        view_missions_service = requests.get(config['Routing']['base_url'] + ':5004/view-missions').text
    except requests.exceptions.ConnectionError:
        return 'View missions service unavailable'
    return render_template('layout.html', html=view_missions_service)


@app.route('/view-mission/<id>')
def view_mission(id):
    try:
        view_mission_service = requests.get(config['Routing']['base_url'] + ':5004/view-mission/' + id).text
    except requests.exceptions.ConnectionError:
        return 'View mission service unavailable'
    return render_template('layout.html', html=view_mission_service)


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
