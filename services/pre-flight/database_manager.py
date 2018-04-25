import configparser

import bson
from bson import ObjectId
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


def get_missions():
    conn = __connect_to_db()
    if conn is None:
        return False

    collection = conn[database].missions
    return collection.find()


def get_mission(id):
    conn = __connect_to_db()
    if conn is None:
        return False, "Could not connect to the database"

    collection = conn[database].missions
    try:
        objectId = ObjectId(id)
        return True, collection.find_one({"_id": objectId})
    except bson.errors.InvalidId:
        return False, "The flight id: " + id + " does not exist"
