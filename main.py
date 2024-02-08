from apimongo import query_sec_api_with_timestamp
from datamongo import read_earliest_timestamp_from_mongo, update_document_in_mongo
from logger import append_to_log
from utils import extract_exhibit_10

def main():
    # Log the start of the main process
    append_to_log("Starting the main process.")

    # Read the earliest timestamp from the JSON file
    earliest_timestamp = read_earliest_timestamp_from_mongo()
    if earliest_timestamp:
        append_to_log(f"Earliest timestamp found: {earliest_timestamp}")
    else:
        append_to_log("No timestamp found; fetching recent filings without date filter.")

    # Query the SEC API with or without a timestamp
    response = query_sec_api_with_timestamp(earliest_timestamp)
    
    if response:
        # Successful API response
        append_to_log("API response received: Success")
        
        # Extract all Exhibit 10 documents for each filing
        all_exhibits = []
        for filing in response.get('filings', []):
            exhibits = extract_exhibit_10(filing)
            all_exhibits.extend(exhibits)

        # Save the extracted data and log the action
        if all_exhibits and update_document_in_mongo(all_exhibits):
            append_to_log(f"Successfully processed and saved {len(all_exhibits)} Exhibit 10 documents.")
        else:
            append_to_log("No new Exhibit 10 documents to process.")
    else:
        # API call failed, log the failure
        append_to_log("API call failed or no data to process")

# Corrected line to check if the script is being run directly
if __name__ == "__main__":
    main()
