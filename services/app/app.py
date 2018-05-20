import argparse
import configparser
import os
import sys
from os import system

import requests
from flask import Flask, render_template, redirect, request
from flask_login import login_required, LoginManager, logout_user, current_user

import database_manager
from login.login import attempt_login
from login.login_form import LoginForm
from login.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

config = configparser.ConfigParser()
services = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))
services.read(os.path.join(os.path.dirname(__file__), '../../services.ini'))


@login_manager.user_loader
def load_user(userid):
    user_exists, user_info = database_manager.get_user(userid)
    return User(user_info['user'], user_info['password'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        if attempt_login(username, password):
            return redirect("/")
    else:
        print(login_form.errors)

    login_page = render_template('login.html', form=login_form)
    return render_template('layout.html', html=login_page)


@app.route('/new-mission')
@login_required
def new_mission():
    auth = current_user.username, current_user.password
    new_mission_request = get_auth("pre_flight", "/new-mission", auth)
    return render_template('layout.html', html=new_mission_request)


@app.route("/save-mission", methods=["POST"])
@login_required
def save_mission():
    data = request.get_data()
    auth = current_user.username, current_user.password
    print(request.content_type[:19] == "multipart/form-data")
    headers = {'Content-Type': request.content_type}
    service_request = post_with_headers_and_auth("pre_flight", "/save-mission", data, headers, auth)
    return service_request


@app.route('/view-missions')
@login_required
def view_missions():
    auth = current_user.username, current_user.password
    view_missions_service = get_auth("post_flight", "/view-missions", auth)
    return render_template('layout.html', html=view_missions_service)


@app.route('/view-mission/<id>')
@login_required
def view_mission(id):
    auth = current_user.username, current_user.password
    view_mission_service = get_auth("post_flight", "/view-mission/" + id, auth)
    return render_template('layout.html', html=view_mission_service)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def get(service, route):
    try:
        url = config['Routing']['base_url'] + ":" + services[service]['port'] + route
        service_request = requests.get(url).text
        return service_request
    except requests.exceptions.ConnectionError:
        return service + " service unavailable"


def get_auth(service, route, auth):
    try:
        url = config['Routing']['base_url'] + ":" + services[service]['port'] + route
        service_request = requests.get(url, auth=auth).text
        return service_request
    except requests.exceptions.ConnectionError:
        return service + " service unavailable"


def post_with_headers_and_auth(service, route, data, headers, auth):
    try:
        url = config['Routing']['base_url'] + ":" + services[service]['port'] + route
        service_request = requests.post(url, data=data, headers=headers, auth=auth).text
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
