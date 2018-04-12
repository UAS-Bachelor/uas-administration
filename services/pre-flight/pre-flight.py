import argparse
import sys
from os import system

from flask import Flask, render_template
from template_parser import load_xml

app = Flask(__name__)


@app.route('/new-mission')
def new_mission():
    return render_template('new-mission.html', message=load_parser(), map=map_service())


#@app.route('/map-service')
def map_service():
    #return render_template('map_service.html')
    return render_template('open_layers_map.html', bufferSize=200)

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
