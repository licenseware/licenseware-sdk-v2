import unittest
from licenseware.history import History
from licenseware.test_helpers.flask_request import get_flask_request


# python3 -m unittest tests/test_history.py

class TestHistory(unittest.TestCase):

    def test_save_filename_validation(self):

        @History.log()
        def validate_filenames(flask_request, name, data):
            """ Validate filenames received """

            response, status_code = {
                        "status": "success",
                        "message": "Filenames are valid",
                        "data": f"{name}, {data}",
                        "validation": [
                            {
                              "status": "success",
                              "filename": "rvtools.xlsx",
                              "message": "Filename is valid"
                            },
                            {
                              "status": "success",
                              "filename": "options.csv",
                              "message": "Filename is valid"
                            }
                          ]
                    }, 200

            return response, status_code

        request = get_flask_request(headers={
            'TenantId': "b37761e3-6926-4cc1-88c7-4d0478b04adf",
            'Authorization': "e9898dfl4s34kjs",
            # 'UploaderId': "rv_tools",
            "X-Forwarded-Path": '/universal-uploader/uploads/universal_uploader/validation'
        })

        response, status_code, headers = validate_filenames(request, "the string", data=[1, 2, 3])

        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], 'success')

        @History.log()
        def processing_function(name, data, filepath,
                                tenant_id="b37761e3-6926-4cc1-88c7-4d0478b04adf",
                                event_id="b37761e3-6926-4cc1-88c7-4d0478b04adf",
                                uploader_id="rv_tools"):
            """ Process data from file """

            response, status_code = {
                                        "status": "success",
                                        "message": "Filenames are valid",
                                        "data": f"{name}, {data}"
                                    }, 200

            return response, status_code

        response, status_code = processing_function("Alin", [1, 2, 3], filepath='path/to/file')

        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], 'success')
