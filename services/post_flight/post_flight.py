import argparse
import json
import os
from datetime import datetime
from os import system

from flask_httpauth import HTTPBasicAuth

import database_manager
import sys
from flask import Flask, render_template
from yattag import Doc

app = Flask(__name__)
auth = HTTPBasicAuth()
doc, tag, text = Doc().tagtext()


@auth.get_password
def get_password(username):
    user_exists, user_info = database_manager.get_user(username)
    if user_exists:
        return user_info['password']
    return None


@app.route('/view-missions')
@auth.login_required
def view_missions():
    missions_list = database_manager.get_missions()
    return render_template('missions-list.html', missions_list=missions_list)


@auth.login_required
@app.route('/view-mission/<id>')
def view_mission(id):
    no_errors, mission = database_manager.get_mission(id)

    if no_errors:
        map = ""
        files = ""
        if "map" in mission:
            map = __build_map(mission['map'])
            del mission['map']

        if "files" in mission:
            files = __build_files(mission['files'])
            del mission['files']
        return render_template('mission.html', mission=mission, map=map, files=files)
    else:
        return render_template('mission.html', error_msg=mission)


def __build_map(map):
    center = map['center']
    radius = map['radius']
    buffer_size = map['bufferSize']
    return render_template('show-mission-map.html', center=center, radius=radius, bufferSize=buffer_size)


def __build_files(files):
    files_html = "Uploaded files: <br />"
    for file in files:
        print(file['name'])
        files_html += "- " + file['name'] + "<br />"
    return files_html


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
        response_to_validate = request_data.files[e]
        save_location = new_dir + "/" + response_to_validate.filename
        response_to_validate.save(save_location)
        files.append({
            'name': e,
            'location': save_location
        })

    if len(files) > 0:
        data_to_save['files'] = files
    return data_to_save


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5005,
                        help='specify which port to run this service on')
    parser.add_argument('-v', '--version', type=float, default=0,
                        help='specify which version of the service this is')
    args = parser.parse_args()
    args.prog = sys.argv[0].split('/')[-1].split('.')[0]

    print('Running {} service version {}'.format(args.prog, args.version))
    system('title {} service version {} on port {}'.format(
        args.prog, args.version, args.port))
    app.run(port=args.port, debug=True)
