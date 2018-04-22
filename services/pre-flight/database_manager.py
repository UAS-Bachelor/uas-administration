import configparser

from pymongo import MongoClient, errors

config = configparser.ConfigParser()
config.read('../../config.ini')


def __connect_to_db():
    try:
        return MongoClient()
    except errors.ConnectionFailure:
        print("Could not connect to db")


def create_mission(mission_details):
    conn = __connect_to_db()
    if conn is None:
        return False
    try:
        collection = conn[config['Database']['database']].missions
        collection.insert_one(mission_details)
        return True
    except errors.OperationFailure:
        print("Could not insert into db")
        return False
