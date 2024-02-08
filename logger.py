import json
import os
from datetime import datetime

def append_to_log(message, log_filename='process_log.json'):
    """Appends a message to the log file with a timestamp."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": message
    }
    try:
        if os.path.exists(log_filename):
            with open(log_filename, 'r+') as file:
                # Load existing log entries, append the new one, and save back to the file.
                log_entries = json.load(file)
                log_entries.append(log_entry)
                file.seek(0)
                file.truncate()
                json.dump(log_entries, file, indent=4)
        else:
            with open(log_filename, 'w') as file:
                # Create the file and save the first log entry.
                json.dump([log_entry], file, indent=4)
        return True
    except Exception as e:
        print(f"Error logging message: {e}")
        return False
