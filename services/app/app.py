from flask import Flask, render_template, request
import requests
import sys
import argparse
from os import system
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    try:
        login = requests.get('http://127.0.0.1:5002/login').text
    except requests.exceptions.ConnectionError:
        return 'Login service unavailable'
    return render_template('layout.html', html=login)


@app.route('/new-mission')
def new_mission():
    try:
        new_mission_request = requests.get('http://127.0.0.1:5004/new-mission').text
    except requests.exceptions.ConnectionError:
        return 'New Mission service unavailable'
    return render_template('layout.html', html=new_mission_request)


@app.route('/map')
def map_service():
    try:
        map_service = requests.get('http://127.0.0.1:5004/map-service').text
    except requests.exceptions.ConnectionError:
        return 'Map service unavailable'
    return render_template('layout.html', html=map_service)


@app.route('/save-mission', methods=['POST'])
def save_mission():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    response_to_validate = request.files['sora']
    form_data = request.files.copy()
    form_list = form_data.keys()
    for e in form_list:
        print(e)
    save_location = current_directory + "/uploads/" + response_to_validate.filename

    response_to_validate.save(save_location)
    #requests.post('http://127.0.0.1:5004/validate-mission', data=response_to_validate)
    return ""

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