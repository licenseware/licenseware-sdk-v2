import unittest 
from licenseware.common.validators.file_validators import validate_filename

# python3 -m unittest tests/test_validate_filename.py


class TestValidateFileName(unittest.TestCase):

    def test_validate_filename(self):

        try:
            valid_filename = True
            validate_filename(
                filename='oracle_name.csv',
                contains=['.+_name\.csv']
            )
        except:
            valid_filename = False

        assert validate_filename
