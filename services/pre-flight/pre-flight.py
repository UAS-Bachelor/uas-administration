import argparse
import json
import os
import sys
from datetime import datetime
from os import system

import AdvancedHTMLParser
from flask import Flask, render_template, request, jsonify
from flask_cors import cross_origin
from yattag import Doc

import database_manager
from template_parser import load_xml

app = Flask(__name__)

doc, tag, text = Doc().tagtext()
parser = AdvancedHTMLParser.AdvancedHTMLParser()


@app.route('/new-mission')
def new_mission():
    return render_template('new-mission.html', message=__load_parser())


@app.route('/view-missions')
def view_missions():
    missions_list = database_manager.get_missions()
    return render_template('missions-list.html', missions_list=missions_list)


@app.route('/view-mission/<id>')
def view_mission(id):
    no_errors, mission = database_manager.get_mission(id)

    if no_errors:
        if "map" in mission:
            map = __build_map(mission['map'])
            del mission['map']

        if "files" in mission:
            files = __build_files(mission['files'])
            del mission['files']
        return render_template('mission.html', mission=mission, map=map, files=files)
    else:
        return render_template('mission.html', error_msg=mission)


@app.route('/save-mission', methods=['POST'])
@cross_origin()
def save_mission():
    save_directory = __get_save_directory()
    mission_to_save = __build_json(request, save_directory)

    result = database_manager.create_mission(mission_to_save)
    if result:
        print("Entry added to db")
    return jsonify(result=result)


def __build_map(map):
    center = map['center']
    radius = map['radius']
    buffer_size = map['bufferSize']
    return render_template('show_mission_map.html', center=center, radius=radius, bufferSize=buffer_size)


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

    data_to_save['files'] = files
    return data_to_save


def __get_save_directory():
    save_directory = os.path.dirname(os.path.realpath(__file__)) + "/uploads/"
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    return save_directory


def __load_parser():
    xml_reference = 'services/pre-flight/template.xml'
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
