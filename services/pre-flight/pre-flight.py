from flask import Flask, render_template
import requests
import sys
import json
import argparse
from os import system

app = Flask(__name__)


@app.route('/new-mission')
def newMission():
    parseJSON()
    return render_template('new-mission.html', message="hi")


def parseJSON():
    reference = 'services/pre-flight/law-template.json'
    with open(reference) as json_file:
        law_template = json.load(json_file)

        for key, child in law_template.items():
            print(key)
            print(child)
saf

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
