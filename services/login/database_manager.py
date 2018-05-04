import configparser

from pymongo import MongoClient, errors

config = configparser.ConfigParser()
config.read('config.ini')
database = config['Database']['database']


def __connect_to_db():
    try:
        return MongoClient()
    except errors.ConnectionFailure as e:
        print("Could not connect to db: %s" % str(e))


def find_user(username):
    global config

    conn = __connect_to_db()
    if conn is None:
        return False, None

    try:
        collection = conn[database].users
        curser = collection.find_one({'username': username})

        if curser is None:
            return False, None

        return True, curser

    except errors.ServerSelectionTimeoutError as e:
        print("Could not connect to db: %s" % str(e))
        return False, None
