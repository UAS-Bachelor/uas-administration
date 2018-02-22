from flask import Flask, render_template
import requests
import sys
import argparse
from os import system

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
def newMission():
    try:
        newMission = requests.get('http://127.0.0.1:5004/new-mission').text
    except requests.exceptions.ConnectionError:
        return 'New Mission service unavailable'
    return render_template('layout.html', html=newMission)

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