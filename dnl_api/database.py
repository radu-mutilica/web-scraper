import pymongo.collection
from pymongo import MongoClient


class MongoDB:
    def __init__(self, db_name: str):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str) -> pymongo.collection.Collection:
        return self.db[collection_name]
