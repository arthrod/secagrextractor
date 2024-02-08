from sec_api import QueryApi
import json

# Replace 'YOUR_API_KEY' with your actual SEC API key
API_KEY = "14ae94994414b7dd507f71bd4fe4c2db2b581f004ea487782ce067d859f62c39"
queryApi = QueryApi(api_key=API_KEY)

def query_sec_api():
    base_query = '(formType:"10-K" OR formType:"10-Q" OR formType:"8-K") AND documentFormatFiles.type:"EX-10"'
    print("Base query constructed.")

    query = {
        "query": {"query_string": {"query": base_query}},
        "from": 0,
        "size": 100,  # Adjust the size as needed
        "sort": [{"filedAt": {"order": "desc"}}]  # Newest filings first
    }
    print("Full query dictionary created.")
    return query

# Use the query function to get the query dictionary
query = query_sec_api()
print("Query to be sent to the SEC API:", query)

# Fetch the filings
response = queryApi.get_filings(query)
print("Response received from the SEC API.")

# Save the raw response to logs2.json
with open('logs2.json', 'w') as log_file:
    json.dump(response, log_file, indent=4)
    print("Raw response saved to logs2.json.")

# Function to check if a file is an Exhibit 10 document
def is_exhibit_10(file):
    # Check if the type starts with "EX-10"
    return file["type"].startswith("EX-10")

# Function to extract Exhibit 10 URLs from a filing
def extract_exhibit_10(filing):
    # Find all Exhibit 10 files in the documentFormatFiles list
    exhibit_10_files = list(filter(is_exhibit_10, filing["documentFormatFiles"]))
    
    # Create a list of exhibits with the desired information
    exhibits = []
    for exhibit in exhibit_10_files:
        exhibits.append({
            "accessionNo": filing["accessionNo"],
            "type": exhibit["type"],
            "url": exhibit["documentUrl"],
            "description": exhibit.get("description", None)  # Use None if description is absent
        })
    return exhibits

# Extract Exhibit 10 URLs from each filing
exhibits = list(map(extract_exhibit_10, response["filings"]))
print("Exhibit 10 URLs extracted from all filings.")

# Flatten the list of lists into a single list
flat_exhibits = [item for sublist in exhibits for item in sublist]
print(f"Flattened the list of exhibits. Total count: {len(flat_exhibits)}")

# Save the flattened exhibits to logs2.json
with open('logs2.json', 'w') as log_file:  # Overwriting the file
    json.dump(flat_exhibits, log_file, indent=4)
    print("Flattened exhibits saved to logs2.json.")
