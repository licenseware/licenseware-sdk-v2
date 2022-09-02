import unittest

from licenseware.registry_service import register_uploader

# python3 -m unittest tests/test_register_uploader.py


payload = {
    "data": [
        {
            "app_id": "odb_222",
            "name": "Flexera Oracle Options",
            "description": "Flexera (LMS OPTIONS) files for Oracle Database.",
            "accepted_file_types": [".csv"],
            "uploader_id": "lms_options_222",
            "flags": [],
            "status": "idle",
            "icon": "default.png",
            "upload_url": "http://localhost:5000/odb/uploads/lms_options/files",
            "upload_validation_url": "http://localhost:5000/odb/uploads/lms_options/validation",
            "quota_validation_url": "http://localhost:5000/odb/uploads/lms_options/quota",
            "status_check_url": "http://localhost:5000/odb/uploads/lms_options/status",
        }
    ]
}


class TestRegisterUploader(unittest.TestCase):
    def test_register_uploader(self):

        data = payload["data"][0]

        response, status_code = register_uploader(**data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
