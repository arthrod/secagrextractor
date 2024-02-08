import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Create a MongoDB client and connect to the database
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def save_processed_data_to_mongo(data):
    """Save processed exhibit data to MongoDB."""
    if data:
        result = collection.insert_many(data)
        return result.acknowledged
    return False

def read_earliest_timestamp_from_mongo():
    """Read the earliest timestamp from the MongoDB database."""
    earliest_document = collection.find_one(sort=[("timestamp", 1)], projection={"timestamp": 1})
    return earliest_document['timestamp'] if earliest_document else None


def update_document_in_mongo(filter_query, update_data):
    """Update a document in the MongoDB database."""
    result = collection.update_one(filter_query, {'$set': update_data})
    return result.modified_count
