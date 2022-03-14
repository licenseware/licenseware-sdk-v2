import unittest
from licenseware.history import History
from licenseware.test_helpers.flask_request import get_flask_request


# python3 -m unittest tests/test_history.py

class TestHistory(unittest.TestCase):

    def test_save_filename_validation(self):


        class UploaderBuilder:

            def __init__(self, uploader_id):
                self.uploader_id = uploader_id

            @History.log()
            def validate_filenames(self, flask_request):
                """ Validate file names provided by user """

                assert self.uploader_id

                response = {
                  "status": "success",
                  "message": "Filenames are valid",
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
                }

                status_code = 200

                return response, status_code


            def upload_files(self, flask_request, event_id=None):
                """ Validate file content provided by user and send files for processing if they are valid """

                header_event_id = flask_request.headers.get("EventId") or event_id
                if header_event_id is None:
                    raise Exception("Parameter `EventId` not provided in headers")

                    return {'status': states.SUCCESS, 'message': 'Event sent', 'event_data': events_data}, 200
                else:
                    event.update({
                        'filepaths': valid_filepaths,
                        'flask_request': {**flask_json, **flask_headers, **flask_args},
                        'validation_response': response
                    })

                    if not validate_event(event, raise_error=False):
                        log.error(event)
                        notify_upload_status(event, status=states.IDLE)
                        return {'status': states.FAILED, 'message': 'Event not valid', 'event_data': event}, 400

                    log.info("Sending event: " + str(event))
                    self.worker.send(event)

                    return {'status': states.SUCCESS, 'message': 'Event sent', 'event_data': event}, 200




        # @History.log()
        # def validate_filenames(flask_request, name, data):
        #     """ Validate filenames received """
        #
        #     response, status_code = {
        #                 "status": "success",
        #                 "message": "Filenames are valid",
        #                 "data": f"{name}, {data}",
        #                 "validation": [
        #                     {
        #                       "status": "success",
        #                       "filename": "rvtools.xlsx",
        #                       "message": "Filename is valid"
        #                     },
        #                     {
        #                       "status": "success",
        #                       "filename": "options.csv",
        #                       "message": "Filename is valid"
        #                     }
        #                   ]
        #             }, 200
        #
        #     return response, status_code
        #
        # request = get_flask_request(headers={
        #     'TenantId': "b37761e3-6926-4cc1-88c7-4d0478b04adf",
        #     'Authorization': "e9898dfl4s34kjs",
        #     # 'UploaderId': "rv_tools",
        #     "X-Forwarded-Path": '/universal-uploader/uploads/universal_uploader/validation'
        # })
        #
        # response, status_code, headers = validate_filenames(request, "the string", data=[1, 2, 3])
        #
        # self.assertEqual(status_code, 200)
        # self.assertEqual(response['status'], 'success')
        #
        # @History.log()
        # def processing_function(name, data, filepath,
        #                         tenant_id="b37761e3-6926-4cc1-88c7-4d0478b04adf",
        #                         event_id="b37761e3-6926-4cc1-88c7-4d0478b04adf",
        #                         uploader_id="rv_tools"):
        #     """ Process data from file """
        #
        #     response, status_code = {
        #                                 "status": "success",
        #                                 "message": "Filenames are valid",
        #                                 "data": f"{name}, {data}"
        #                             }, 200
        #
        #     return response, status_code
        #
        # response, status_code = processing_function("Alin", [1, 2, 3], filepath='path/to/file')
        #
        # self.assertEqual(status_code, 200)
        # self.assertEqual(response['status'], 'success')
