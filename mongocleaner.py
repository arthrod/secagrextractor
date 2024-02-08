from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Create a MongoDB client and connect to the database
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def remove_duplicate_documents():
    # Define the aggregation pipeline to identify duplicates
    pipeline = [
        {
            "$group": {
                "_id": "$url",  # Group by the "url" field
                "duplicateIds": {
                    "$push": "$_id"  # Push all "_id"s into an array
                },
                "count": {"$sum": 1}  # Count the number of duplicates
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}  # Match groups with more than one document
            }
        }
    ]

    # Run the aggregation pipeline
    duplicates = list(collection.aggregate(pipeline))

    # Iterate over the results and delete duplicates, keeping only the first document
    for duplicate in duplicates:
        duplicate_ids = duplicate["duplicateIds"]
        # Skip the first ID to keep one document and remove the rest
        for dup_id in duplicate_ids[1:]:
            collection.delete_one({"_id": dup_id})

    print(f"Removed duplicates based on the 'url' field.")

if __name__ == "__main__":
    remove_duplicate_documents()
