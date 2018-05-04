import argparse
import sys
import json
from os import system

import database_manager
from flask import Flask, request

app = Flask(__name__)


@app.route("/login", methods=['POST'])
def login():
    data = json.loads(request.get_data())
    username = data['username']
    return check_for_user(username)


def check_for_user(username):
    result, user = database_manager.find_user(username)
    if result:
        return "User exists"
    else:
        return "User does not exist"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5001,
                        help='specify which port to run this service on')
    parser.add_argument('-v', '--version', type=float, default=0,
                        help='specify which version of the service this is')
    args = parser.parse_args()
    args.prog = sys.argv[0].split('/')[-1].split('.')[0]

    print('Running {} service version {}'.format(args.prog, args.version))
    system('title {} service version {} on port {}'.format(
        args.prog, args.version, args.port))
    app.run(port=args.port, debug=True)
