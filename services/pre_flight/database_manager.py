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


def create_mission(mission_details):
    global config

    conn = __connect_to_db()
    if conn is None:
        return False
    try:
        collection = conn[database].missions
        collection.insert_one(mission_details)
        return True
    except errors.OperationFailure as e:
        print("Could not insert into db: %s" % str(e))
        return False
    except errors.ServerSelectionTimeoutError as e:
        print("Could not connect to db: %s" % str(e))
        return False
