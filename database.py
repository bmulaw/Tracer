import os
from typing import Any

from pymongo import MongoClient

from rules import extract_company_identifiers

def _store_raw(key: str, value: Any) -> None:
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
        print("added raw", key, "to mongodb")
    finally:
        client.close()

def _store_cleaned(key: str, value: Any) -> None:
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
        print("added cleaned", key, "to mongodb")
    finally:
        client.close()


def store(key: str, value: list[str]) -> list[str]:
    """
        Key: the key for the mongodb record
        Value: the value for the key to be stored in mongodb
    """
    cleaned_company_ids = extract_company_identifiers(value)
    _store_raw(key=key, value=value)
    _store_cleaned(key=key, value=cleaned_company_ids)
    return cleaned_company_ids
