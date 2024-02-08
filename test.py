import unittest
from unittest.mock import patch, mock_open
from data import read_earliest_timestamp_from_json, save_processed_data
from utilsold import is_exhibit_10, extract_exhibit_10
from api import query_sec_api

# Mock data for testing
mock_json_data = [
    {
        "newid": "123",
        "accessionNo": "0000000000",
        "type": "EX-10",
        "url": "http://example.com/ex-10",
        "timestamp": "2021-04-01T00:00:00Z"
    },
    # ... add more mock data if needed
]

class TestDataMethods(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(mock_json_data))
    def test_read_earliest_timestamp_from_json(self, mock_file):
        # Test the function that reads the earliest timestamp from a JSON file
        timestamp = read_earliest_timestamp_from_json('testfile.json')
        self.assertEqual(timestamp, "2021-04-01T00:00:00Z")

    # more tests to be added here...

class TestUtilsMethods(unittest.TestCase):

    def test_is_exhibit_10(self):
        # Test the function that checks if a file is an Exhibit 10
        example_file = {"type": "EX-10"}
        self.assertTrue(is_exhibit_10(example_file))

    # more tests to be added here...

# other test classes...

if __name__ == '__main__':
    unittest.main()
