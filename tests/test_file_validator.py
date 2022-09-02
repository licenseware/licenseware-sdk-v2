import unittest

from licenseware.common.validators.file_validators import validate_text_contains_any

# python3 -m unittest tests/test_file_validator.py


class TestFileValidator(unittest.TestCase):
    def test_validate_text_contains_any(self):

        text = """        

        10g DBA_FEATURE_USAGE_STATISTICS
        ------------------------------------------    
                
        *** PARTITIONING
        ======================================================================

        ORACLE PARTITIONING INSTALLED: TRUE
        
        DATABASE VERSION
        ------------------------------------------
        
        """

        keywords = [
            "DBA_FEATURE_USAGE_STATISTICS",
            "ORACLE PARTITIONING INSTALLED",
            "DATABASE VERSION",
        ]

        validate_text_contains_any(text, keywords)

        intended_fail = False

        try:
            validate_text_contains_any("no match here", ["empty"])
        except:
            intended_fail = True

        assert intended_fail
