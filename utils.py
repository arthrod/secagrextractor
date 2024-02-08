import re
import uuid

def is_exhibit_10(file):
    # Use startswith instead of regex for simplicity and reliability
    return file["type"].startswith("EX-10")

def extract_exhibit_10(filing):
    """Extracts exhibit 10 documents from a filing."""
    # Find all Exhibit 10 files in the documentFormatFiles list
    exhibit_10_files = list(filter(is_exhibit_10, filing.get("documentFormatFiles", [])))

    # Create a list of exhibits with the desired information
    exhibits = []  # Ensure that this is always initialized as a list
    for exhibit in exhibit_10_files:
        exhibits.append({
            "accessionNo": filing["accessionNo"],
            "type": exhibit["type"],
            "url": exhibit["documentUrl"],
            "description": exhibit.get("description", "N/A"),  # Use "N/A" if description is absent
            "_id": str(uuid.uuid4()),  # Generate a unique identifier for each exhibit
            "timestamp": filing["filedAt"]  # Add the 'filedAt' timestamp from the filing
        })
    return exhibits  # Ensure that this always returns a list, even if it's empty


