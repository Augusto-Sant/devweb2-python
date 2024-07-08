from pymongo import MongoClient
from utils import MONGO_CONNECTION_URL, MONGO_DATABASE
from fastapi import Depends


def get_mongo_client():
    client = MongoClient(MONGO_CONNECTION_URL)
    try:
        yield client
    finally:
        client.close()


def get_database(client: MongoClient = Depends(get_mongo_client)):
    return client[MONGO_DATABASE]
