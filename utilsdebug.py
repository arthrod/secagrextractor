import re
import uuid

def is_exhibit_10(file):
    # Regex pattern to match 'EX-10' or 'EX-10' followed by a dot and any characters
    pattern = r"EX-10(\..+)?$"
    match = re.match(pattern, file["type"], re.I)
    if match:
        print(f"Debug: Match found for {file['type']}")
    else:
        print(f"Debug: No match found for {file['type']}")
    return match is not None

def extract_exhibit_10(filing):
    """Extracts exhibit 10 documents from a filing."""
    # ... (rest of the code remains the same)
