import io
import os
import unittest

from werkzeug.datastructures import FileStorage

from licenseware.uploader_validator import UploaderValidator

from . import tenant_id

# python3 -m unittest tests/test_uploader_validator.py


files_path = "/home/acmt/Documents/files_test/test_validators_files"
mock_filenames = [
    "rvtools.xlsx",
    "rv_tools.xlsx",
    "randomfile.pdf",
    "skip_this_file.csv",
]

# Simulating a flask request object
class flask_request:

    json = mock_filenames

    class files:
        @classmethod
        def getlist(cls, key):

            if key != "files[]":
                raise Exception("Key 'files[]' doesn't exist")

            mock_binary_files = []
            for fname in mock_filenames:

                with open(os.path.join(files_path, fname), "rb") as f:
                    file_binary = io.BytesIO(f.read())

                mock_file = FileStorage(
                    stream=file_binary,
                    filename=fname,
                    content_type="application/*",
                )

                mock_binary_files.append(mock_file)

            return mock_binary_files

    class headers:
        @classmethod
        def get(cls, tenant_id_param):
            return tenant_id


class TestUploadValidator(unittest.TestCase):
    def setUp(self):
        self.assertEqual.__self__.maxDiff = None

    def test_validate_filenames(self):

        rv_tools_validator = UploaderValidator(
            # _uploader_id = 'rv_tools',
            filename_contains=["RV", "Tools"],
            filename_endswith=[".xls", ".xlsx"],
            ignore_filenames=["skip_this_file.csv"],
            required_input_type="excel",
            min_rows_number=1,
            required_sheets=["tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"],
            required_columns=[
                "VM",
                "Host",
                "OS",
                "Sockets",
                "CPUs",
                "Model",
                "CPU Model",
                "Cluster",
                "# CPU",
                "# Cores",
                "ESX Version",
                "HT Active",
                "Name",
                "NumCpuThreads",
                "NumCpuCores",
            ],
        )

        response, status_code = rv_tools_validator.get_filenames_response(flask_request)
        # print(response)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")

        response, status_code = rv_tools_validator.get_file_objects_response(
            flask_request
        )
        self.assertEqual(status_code, 200)
        # print(response)
        self.assertEqual(response["status"], "success")

        file_paths = rv_tools_validator.get_filepaths_from_objects_response(response)
        # print(file_paths)

        [self.assertEqual(os.path.exists(fp), True) for fp in file_paths]
