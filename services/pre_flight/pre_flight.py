import argparse
import json
import os
import sys
from datetime import datetime
from os import system

from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from flask_httpauth import HTTPBasicAuth
from yattag import Doc
from flask_basicauth import BasicAuth

import database_manager
from template_parser import load_xml

app = Flask(__name__)

auth = HTTPBasicAuth()

doc, tag, text = Doc().tagtext()
template_to_use = "template.xml"


@auth.get_password
def get_password(username):
    user_exists, user_info = database_manager.get_user(username)
    if user_exists:
        return user_info['password']
    return None


@app.route('/new-mission')
@auth.login_required
def new_mission():
        return render_template('new-mission.html', message=__load_parser())


@app.route('/save-mission', methods=['POST'])
@cross_origin()
def save_mission():
    save_directory = __get_save_directory()
    mission_to_save = __build_json(request, save_directory)

    result = database_manager.create_mission(mission_to_save)
    return jsonify(result=result)


def __build_json(request_data, save_directory):
    data_to_save = {}
    files = []

    current_time = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    data_to_save['time'] = current_time

    form_data = request_data.form.copy()
    form_list = form_data.keys()
    for key in form_list:
        try:
            parsed_value = json.loads(form_data[key])
            data_to_save[key] = parsed_value
        except ValueError:
            data_to_save[key] = form_data[key]

    form_data_files = request_data.files.copy()
    form_list_files = form_data_files.keys()
    new_dir = save_directory + current_time
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for e in form_list_files:
        save_location = __save_file(request_data.files[e], new_dir)
        files.append({
            'name': e,
            'location': save_location
        })

    if len(files) > 0:
        data_to_save['files'] = files
    return data_to_save


def __save_file(file, save_dir):
    response_to_validate = file
    save_location = save_dir + "/" + response_to_validate.filename
    response_to_validate.save(save_location)
    return save_location


def __get_save_directory():
    save_directory = os.path.dirname(os.path.realpath(__file__)) + "/uploads/"
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    return save_directory


def __load_parser():
    xml_reference = os.path.join(os.path.dirname(__file__), template_to_use)
    return load_xml(xml_reference)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5004,
                        help='specify which port to run this service on')
    parser.add_argument('-v', '--version', type=float, default=0,
                        help='specify which version of the service this is')
    args = parser.parse_args()
    args.prog = sys.argv[0].split('/')[-1].split('.')[0]

    print('Running {} service version {}'.format(args.prog, args.version))
    system('title {} service version {} on port {}'.format(
        args.prog, args.version, args.port))
    app.run(port=args.port, debug=True)
