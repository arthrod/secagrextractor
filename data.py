import json
import os

def read_earliest_timestamp_from_json(filename='exhibit_10_urls.json'):
    """Reads the earliest timestamp from the specified JSON file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            earliest_timestamp = data[-1]['timestamp'] if data else None
            return earliest_timestamp
    except FileNotFoundError:
        return None
    except KeyError:
        earliest_timestamp = None  # Handle missing 'timestamp' key


def save_processed_data(data, filename='exhibit_10_urls.json'):
    """Saves processed data to a specified file."""
    try:
        if os.path.exists(filename):
            with open(filename, 'r+') as file:
                existing_data = json.load(file)
                existing_data.extend(data)
                file.seek(0)
                file.truncate()
                json.dump(existing_data, file, indent=4)
        else:
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        print(f"Saved processed data to {filename}.")
    except Exception as e:
        print(f"Error saving processed data: {str(e)}")
