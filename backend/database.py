from pymongo import MongoClient

from backend.config import settings

client = MongoClient(settings.mongo_uri)
db = client["luxe_shop"]