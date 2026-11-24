"""Shared, lazily connected MongoDB client."""
from functools import lru_cache
from django.conf import settings
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_database():
    config = settings.MONGO_CONNECTION
    client = MongoClient(config["HOST"], serverSelectionTimeoutMS=5000)
    return client[config["DB"]]


def get_collection(kind):
    return get_database()[settings.MONGO_CONNECTION[f"{kind.upper()}_COLLECTION"]]
