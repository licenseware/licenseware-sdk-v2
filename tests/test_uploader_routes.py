import io
import os
import re
import unittest

from main import app
from werkzeug.datastructures import FileStorage

from licenseware.common.constants import envs
from licenseware.uploader_validator import UploaderValidator
from licenseware.utils.logger import log

from . import headers

# python3 -m unittest tests/test_uploader_routes.py


app_routes = [str(rule) for rule in app.url_map.iter_rules()]

for path in app_routes:
    m = re.search(f"/.*/uploads/(.*)/validation", path)
    if m:
        uploader_id = m.group(1)
        break


prefix = envs.APP_ID
pathto = lambda route: prefix + route


upload_validation_path = f"/uploads/{uploader_id}/validation"
upload_path = f"/uploads/{uploader_id}/files"
quota_validation_path = f"/uploads/{uploader_id}/quota"
status_check_path = f"/uploads/{uploader_id}/status"


def get_mock_binary_files():

    files_path = "/home/acmt/Documents/files_test/test_validators_files"
    mock_filenames = [
        "rvtools.xlsx",
        "rv_tools.xlsx",
        "randomfile.pdf",
        "skip_this_file.csv",
    ]
    # 'rvtools.xlsx', "rv_tools.xlsx" are valid filenames

    mock_binary_files = []
    for fname in mock_filenames:

        with open(os.path.join(files_path, fname), "rb") as f:
            file_binary = io.BytesIO(f.read())

        mock_file = FileStorage(
            stream=file_binary,
            filename=fname,
            content_type="application/*",
        )

        mock_binary_files.append((mock_file, fname))

    return {"files[]": mock_binary_files}


class TestUploaderRoutes(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_filenames_validation_route(self):

        url = pathto(upload_validation_path)

        filenames_to_validate = ["rvtools.xlsx", "rv_tools.xlsx", "randomfile.pdf"]

        response = self.app.post(url, headers=headers, json=filenames_to_validate)

        log.debug(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(len(response.json["validation"]), len(filenames_to_validate))

    def test_files_upload_route(self):

        url = pathto(upload_path)

        mock_binary_files = get_mock_binary_files()

        response = self.app.post(url, headers=headers, data=mock_binary_files)

        log.warning(response.json)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        # 2 files have valid names in get_mock_binary_files func
        self.assertEqual(len(response.json["validation"]), 2)

        file_paths = UploaderValidator.get_filepaths_from_objects_response(
            response.json
        )

        [self.assertEqual(os.path.exists(fp), True) for fp in file_paths]
