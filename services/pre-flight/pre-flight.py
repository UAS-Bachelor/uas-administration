import argparse
import json
import sys
from os import system

from flask import Flask, render_template, request
from requirements_parser import parse_json

app = Flask(__name__)


@app.route('/new-mission')
@app.route('/new-mission/<int:identifier>')
def new_mission(identifier=None):
    #print(request.args.get('x', ''))
    #print(identifier)
    return render_template('new-mission.html', message=load_json())


'''@app.route('/new-mission', methods=['POST'])
def update_new_mission():
    return ""
'''

def load_json():
    reference = 'services/pre-flight/law-template.json'
    with open(reference, encoding='utf-8') as json_file:
        law_template = json.load(json_file)
        return parse_json(law_template)


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
