import os
import unittest

from main import App, app

from licenseware.common.constants import envs
from licenseware.utils.logger import log

from . import headers

# python3 -m unittest tests/test_filename_validation_rv_tools.py


uploader_id = "rv_tools"


class Testrv_toolsName(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_filename_validation(self):

        url = None
        for uploader in App.uploaders:
            if uploader.uploader_id == uploader_id:
                url = envs.APP_PATH + envs.UPLOAD_PATH + uploader.upload_validation_path
                break

        filenames_to_validate = os.listdir(f"test_files/{uploader_id}")

        log.info(url)
        log.info(filenames_to_validate)

        self.assertNotEqual(url, None)

        response = self.app.post(url, headers=headers, json=filenames_to_validate)

        log.debug(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(len(response.json["validation"]), len(filenames_to_validate))

        for res in response.json["validation"]:
            self.assertEqual(res["status"], "success")
