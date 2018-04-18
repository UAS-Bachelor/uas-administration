import argparse
import sys
from os import system
import AdvancedHTMLParser
import os
from datetime import datetime
from flask_cors import cross_origin
import json

from flask import Flask, render_template, request
from template_parser import load_xml
from yattag import Doc, indent

app = Flask(__name__)

doc, tag, text = Doc().tagtext()
parser = AdvancedHTMLParser.AdvancedHTMLParser()


@app.route('/new-mission')
def new_mission():
    return render_template('new-mission.html', message=load_parser())


@app.route('/save-mission', methods=['POST'])
@cross_origin()
def save_mission():
    current_directory = os.path.dirname(os.path.realpath(__file__)) + "/uploads/"
    if not os.path.exists(current_directory):
        os.mkdir(current_directory)

    data_to_save = {}
    files = []

    form_data = request.form.copy()
    form_list = form_data.keys()
    for key in form_list:
        data_to_save[key] = form_data[key]
    form_data_files = request.files.copy()
    form_list_files = form_data_files.keys()
    current_time = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    new_dir = current_directory + current_time
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for e in form_list_files:
        print(e)
        response_to_validate = request.files[e]
        save_location = new_dir + "/" + response_to_validate.filename
        response_to_validate.save(save_location)
        files.append({
            'name': e,
            'location': save_location
        })

    data_to_save['files'] = files
    json_data = json.dumps(data_to_save)
    print(json_data)
    return ""


def load_parser():
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
