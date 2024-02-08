from apimongo import query_sec_api_with_timestamp
from datamongo import read_earliest_timestamp_from_mongo, save_processed_data_to_mongo
from logger import append_to_log
from utils import extract_exhibit_10
import traceback

def main():
    try:
        # Read the earliest timestamp from the MongoDB database
        earliest_timestamp = read_earliest_timestamp_from_mongo()
        if earliest_timestamp:
            append_to_log(f"Earliest timestamp found: {earliest_timestamp}")
        else:
            append_to_log("No timestamp found; fetching recent filings without date filter.")

        # Call the function without passing the timestamp
        response = query_sec_api_with_timestamp()

        if response:
            # Successful API response
            append_to_log("API response received: Success")

            # Extract all Exhibit 10 documents for each filing
            all_exhibits = []
            for filing in response.get('filings', []):
                exhibits = extract_exhibit_10(filing)
                all_exhibits.extend(exhibits)

            # Save the extracted data to MongoDB and log the action
            if all_exhibits and save_processed_data_to_mongo(all_exhibits):
                append_to_log(f"Successfully processed and saved {len(all_exhibits)} Exhibit 10 documents to MongoDB.")
            else:
                append_to_log("No new Exhibit 10 documents to process or failed to save to MongoDB.")
        else:
            # API call failed, log the failure
            append_to_log("API call failed or no data to process")

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        append_to_log(error_message)
        # Log the full traceback for debugging purposes
        traceback_details = traceback.format_exc()
        append_to_log(traceback_details)

# Corrected line to check if the script is being run directly
if __name__ == "__main__":
    main()
