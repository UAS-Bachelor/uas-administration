import argparse
import sys
from os import system
import AdvancedHTMLParser

from flask import Flask, render_template, request
from template_parser import load_xml
from yattag import Doc, indent

app = Flask(__name__)
doc, tag, text = Doc().tagtext()
parser = AdvancedHTMLParser.AdvancedHTMLParser()


@app.route('/new-mission')
def new_mission():
    return render_template('new-mission.html', message=load_parser())


@app.route('/validate-mission', methods=['POST'])
def validate():
    print(request.get_data())
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
