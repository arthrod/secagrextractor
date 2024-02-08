import os
from sec_api import QueryApi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Load the environment variable from the .env file.
load_dotenv()
API_KEY = os.getenv('SEC_API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

query_api = QueryApi(api_key=API_KEY)

# Create a MongoDB client and connect to the database
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def get_earliest_timestamp():
    earliest_document = collection.find_one(sort=[("timestamp", 1)])
    return earliest_document['timestamp'] if earliest_document else None


def query_sec_api_with_timestamp():
    earliest_timestamp = get_earliest_timestamp()
    
    base_query = '(formType:"10-K" OR formType:"10-Q" OR formType:"8-K") AND documentFormatFiles.type:"EX-10"'
    
    if earliest_timestamp:
        # Format the timestamp if necessary or use as is if the API supports your format
        base_query += f' AND filedAt:{{* TO "{earliest_timestamp}"}}'

    query = {
        "query": {"query_string": {"query": base_query}},
        "from": 0,
        "size": 50,
        "sort": [{"filedAt": {"order": "desc"}}]  # Assuming you want the latest filings first
    }
    
    try:
        response = query_api.get_filings(query)
        return response
    except Exception as e:
        print(f"API call error: {str(e)}")
        return None
