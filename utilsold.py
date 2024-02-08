import re
import uuid

def is_exhibit_10(file):
    # Updated regex pattern to match 'EX-10' or 'EX-10' followed by a dot and anything after it
    pattern = r"EX-10(\..+)?$"
    return bool(re.match(pattern, file["type"], re.I))

def extract_exhibit_10(filing):
    """Extracts exhibit 10 documents from a filing."""
    exhibit_10_files = list(filter(is_exhibit_10, filing.get("documentFormatFiles", [])))
    exhibits = []
    for exhibit in exhibit_10_files:
        exhibits.append({
            "newid": str(uuid.uuid4()), # Generate a unique identifier for each exhibit
            "accessionNo": filing["accessionNo"],
            "type": exhibit["type"],
            "url": exhibit["documentUrl"],
            "timestamp": filing.get("filedAt") # Add 'filedAt' from the filing as 'timestamp'
        })
    return exhibits
