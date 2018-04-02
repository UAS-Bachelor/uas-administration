import argparse
import json
import sys
from os import system
import AdvancedHTMLParser

from flask import Flask, render_template, render_template_string
from requirements_parser import parseJSON
from yattag import Doc, indent

app = Flask(__name__)
doc, tag, text = Doc().tagtext()
parser = AdvancedHTMLParser.AdvancedHTMLParser()


@app.route('/new-mission')
def newMission():
    # loadJSON()
    with tag('head'):
        with tag('script', src="__javascript__/test.js"):
            pass
    with tag('body'):
        with tag('button', id='testMe', onclick='test.varToTest.changeText()'):
            text("Tryk på mig")
        with tag('h1', id='test1'):
            text("Default text")

    return render_template_string(doc.getvalue())


class SomeTest:
    def changeText(self):
        print("Går ind i metode")
        parser.getElementById('test1').innerHTML = 'Ny tekst - Det virker!'


varToTest = SomeTest()


def loadJSON():
    reference = 'services/pre-flight/law-template.json'
    with open(reference) as json_file:
        law_template = json.load(json_file)
        return parseJSON(law_template)


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
