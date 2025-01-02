# services/mongo_service.py

from pymongo import MongoClient
from config import MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['mydatabase']  # Replace with your MongoDB database name

def insert_data(collection_name, data):
    collection = db[collection_name]
    result = collection.insert_one(data)
    return result.inserted_id

def get_data(collection_name):
    collection = db[collection_name]
    return list(collection.find())
