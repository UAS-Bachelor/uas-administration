import configparser
import os

from pymongo import MongoClient, errors

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../../config.ini'))
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
        return False, "Could not connect to db"
    try:
        collection = conn[database].missions
        collection.insert_one(mission_details)
        return True, "Mission created"
    except errors.OperationFailure as e:
        return False, "Could not insert into db: %s" % str(e)
    except errors.ServerSelectionTimeoutError as e:
        return False, "Could not connect to db: %s" % str(e)
