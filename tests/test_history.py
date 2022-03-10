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
                "data": f"{name}, {data}"
            }, 200

            return response, status_code

        request = get_flask_request(headers={
            'TenantId': "1234",
            'Authorization': "e9898dfl4s34kjs"
        })

        response, status_code = validate_filenames(request, "the string", data=[1,2,3])

        self.assertEqual(status_code, 200)
        self.assertEqual(response['status'], 'success')

        # @History.log()
        # def validate_something(name, data):
        #     pass
        #
        # result = validate_something("name", "data")





