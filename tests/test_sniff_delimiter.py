import unittest
import glob
from licenseware.common.validators.file_validators import GeneralValidator

# python3 -m unittest tests/test_sniff_delimiter.py

class TestSniffDelimiter(unittest.TestCase):
    
    def test_sniff_delimiter(self):
        result_map = {
            "semicolon.csv": ";",
            "comma.csv": ",",
            "pipe.csv": ","
        }
        mock_data = glob.glob("tests/test_data/sniff_delimiter/*.csv")
        
        for file in mock_data:
            general_validator = GeneralValidator(
                input_object = file
            )
            self.assertEqual(general_validator._sniff_delimiter(), result_map[file.split("/")[-1]])
