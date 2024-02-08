import os
from sec_api import QueryApi
from dotenv import load_dotenv

# Load the environment variable from the .env file.
load_dotenv()
API_KEY = os.getenv('SEC_API_KEY')

query_api = QueryApi(api_key=API_KEY)

def query_sec_api(before_timestamp=None):
    base_query = '(formType:"10-K" OR formType:"10-Q" OR formType:"8-K") AND documentFormatFiles.type:"EX-10"'
    
    if before_timestamp:
        # Format the timestamp if necessary or use as is if the API supports your format
        base_query += f' AND filedAt:{{* TO "{before_timestamp}"}}'

    query = {
        "query": {"query_string": {"query": base_query}},
        "from": 0,
        "size": 50,
        "sort": [{"filedAt": {"order": "desc"}}]  # Assuming you want the oldest filings first
    }
    
    try:
        response = query_api.get_filings(query)
        return response
    except Exception as e:
        print(f"API call error: {str(e)}")
        return None
