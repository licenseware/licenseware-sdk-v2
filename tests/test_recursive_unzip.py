import os
import unittest

from licenseware.utils.file_utils import recursive_unzip

# python3 -m unittest tests/test_recursive_unzip.py


class TestRecursiveUnzip(unittest.TestCase):
    def test_recursive_unzip(self):

        test_files_path = "test_files/lms_db_collection"

        filespaths = [
            os.path.abspath(os.path.join(test_files_path, fname))
            for fname in os.listdir(test_files_path)
        ]

        unziped_paths = []
        for fpath in filespaths:
            # log.info(fpath)
            unziped_path = recursive_unzip(fpath)
            unziped_paths.append(unziped_path)

        # log.info(unziped_paths)

        for upath in unziped_paths:
            assert os.path.exists(upath)
