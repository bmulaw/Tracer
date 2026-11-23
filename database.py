import os
from typing import Any

from pymongo import MongoClient

def store_raw(key: str, value: Any) -> None:
    """
        Key: the key for the mongodb record
        Value: the value for the key to be stored in mongodb
    """
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    try:
        collection = client[
            os.getenv("MONGODB_DATABASE", "trace_db")
        ][os.getenv("MONGODB_COLLECTION", "traced_sites_raw")]
        collection.replace_one(
            {"_id": key}, {"_id": key, "value": value}, upsert=True
        )
        print("added", key, "to mongodb")
    finally:
        client.close()

def store_cleaned(key: str, value: Any) -> None:
    """
        Key: the key for the mongodb record
        Value: the value for the key to be stored in mongodb
    """
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    try:
        collection = client[
            os.getenv("MONGODB_DATABASE", "trace_db")
        ][os.getenv("MONGODB_COLLECTION", "traced_sites")]
        collection.replace_one(
            {"_id": key}, {"_id": key, "value": value}, upsert=True
        )
        print("added", key, "to mongodb")
    finally:
        client.close()