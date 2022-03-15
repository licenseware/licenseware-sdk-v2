import os
import unittest
import traceback
from licenseware import history
from licenseware.test_helpers.flask_request import get_flask_request


# python3 -m unittest tests/test_history.py

class TestHistory(unittest.TestCase):

    def test_uploader_builder(self):

        class UploaderBuilder:

            def __init__(self, uploader_id):
                self.uploader_id = uploader_id

            @history.log()
            def validate_filenames(self, flask_request):
                """ Validate file names provided by user """

                assert self.uploader_id

                response = {
                  "status": "success",
                  "message": "Filenames are valid",
                  "validation": [
                    {
                      "status": "success",
                      "filename": "cpuq.txt",
                      "message": "Filename is valid"
                    }
                  ]
                }

                status_code = 200

                return response, status_code

            @history.log()
            def upload_files(self, flask_request, event_id=None):
                """ Validate file content provided by user and send files for processing if they are valid """

                header_event_id = flask_request.headers.get("EventId") or event_id
                if header_event_id is None:
                    raise Exception("Parameter `EventId` not provided in headers")

                fn = "cpuq.txt"
                fp = "/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf"
                if not os.path.exists(fp): os.makedirs(fp)
                with open(os.path.join(fp, fn), "w") as f:
                    f.write("testfile")

                response = {
                        "status": "success",
                        "message": "Event sent",
                        "event_data": {
                            "tenant_id": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
                            "uploader_id": "universal_uploader",
                            "event_id": header_event_id,
                            "filepaths": [
                                "/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt"
                            ],
                            "flask_request": {
                                "Host": "localhost",
                                "Connection": "keep-alive",
                                "X-Forwarded-For": "172.18.0.1",
                                "X-Forwarded-Proto": "http",
                                "X-Forwarded-Host": "localhost",
                                "X-Forwarded-Port": "80",
                                "X-Forwarded-Path": "/universal-uploader/uploads/universal_uploader/files",
                                "X-Real-Ip": "172.18.0.1",
                                "Content-Length": "6655",
                                "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
                                "Sec-Ch-Ua-Mobile": "?0",
                                "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDc0MTA3NDIsImlhdCI6MTY0NzMyNDMzNywic3ViIjoiMzc0MmQ4ODgtNzNjNS00MTA1LTk4OTgtYjIwZjZhMmNlMjM1In0.AB8XcpdcHUuEWdT1OCoPlawGlo---04Aao1dGzfBcnM",
                                "Tenantid": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
                                "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryi05iYC9qUsw1HPnC",
                                "Accept": "application/json",
                                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                                "Sec-Ch-Ua-Platform": "\"Linux\"",
                                "Origin": "http://localhost",
                                "Sec-Fetch-Site": "same-origin",
                                "Sec-Fetch-Mode": "cors",
                                "Sec-Fetch-Dest": "empty",
                                "Referer": "http://localhost/universal-uploader/docs",
                                "Accept-Encoding": "gzip, deflate, br",
                                "Accept-Language": "en-US,en;q=0.9,ro;q=0.8,it;q=0.7,fr;q=0.6",
                                "Cookie": "PGADMIN_LANGUAGE=en; username-localhost-8889=\"2|1:0|10:1646133817|23:username-localhost-8889|44:ZTZkMjJhN2NkZWM2NDNmZDkxYTVkNTVjYTg0NjRlM2E=|38b7f9e169bfa62662aa3ff1d146050f2964b793dc3902120ba90c4e20535626\"; username-localhost-8888=\"2|1:0|10:1646996386|23:username-localhost-8888|44:MmQzODg2ODhjY2E0NDY1Yzg1Y2FhOWUwY2EzYjRlZDY=|e72eb76bbecc87382940894602d81bb601977e231173ac0d2922d8fc4b1218b4\"; _xsrf=2|3ea9ea76|6ebac8ec76a4cd27fed85d0eb847f7bd|1646996386; mongo-express=s%3AVAettPkb_tNq0EZQcZqY96UKMb4vQ_s1.m02RdaZSFY5qVSrgPU%2FkfwHsrhojQX0P8gGOnjMZ1Ys"
                            },
                            "validation_response": {
                                "tenant_id": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
                                "status": "success",
                                "message": "Files are valid",
                                "validation": [
                                    {
                                        "status": "success",
                                        "filename": "cpuq.txt",
                                        "filepath": "/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt",
                                        "message": "Filename is valid"
                                    }
                                ]
                            }
                        }
                    }

                status_code = 200

                return response, status_code


        ub = UploaderBuilder("cpuq")

        fn_request = get_flask_request(
            headers={
                "TenantId": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
                "Authorization": "asdkjfdsiu4kjds"
            },
            json={
                "filenames": ["cpuq.txt"]
            }
        )

        fn_response, fn_status_code, fn_headers = ub.validate_filenames(fn_request)

        # print(fn_response, fn_status_code, fn_headers)

        fc_request = get_flask_request(
            headers={
                "TenantId": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
                "Authorization": "asdkjfdsiu4kjds",
                "EventId": fn_headers["EventId"]
            },
            json={
                "filenames": ["cpuq.txt"]
            }
        )

        fc_response, fc_status_code, fc_headers = ub.upload_files(fc_request)

        # print(fc_response, fc_status_code, fc_headers)

        # On the worker side we need to get `event_id`, `uploader_id`, `tenant_id`, `filepaths` from the even received

        # @history.log()
        # def processing_function(filepath, event_id, uploader_id, tenant_id):
        #     """ Getting some data out of provided cpuq.txt file """
        #     print(f"Processing {filepath}...")
        #     print("Done!")
        #     return {"k": "v"}
        #
        # for filepath in fc_response["event_data"]["filepaths"]:
        #     data = processing_function(
        #         filepath=filepath,
        #         event_id=fc_response["event_data"]["event_id"],
        #         uploader_id=fc_response["event_data"]["uploader_id"],
        #         tenant_id=fc_response["event_data"]["tenant_id"]
        #     )
        #
        #     print(data)

        def processing_function_without_decorator(filepath, event_id, uploader_id, tenant_id):
            """ Getting some data out of provided cpuq.txt file """
            print(f"Processing {filepath}...")

            try:
                raise Exception("Something bad happened")
            except Exception as error:
                history.log_failure(
                    func=processing_function_without_decorator, # for classes use self.func
                    tenant_id=tenant_id,
                    event_id=event_id,
                    uploader_id=uploader_id,
                    filepath=filepath,
                    error_string=str(error),
                    traceback_string=str(traceback.format_exc())
                )

            print("Done!")
            return {"k": "v"}

        for filepath in fc_response["event_data"]["filepaths"]:
            data = processing_function_without_decorator(
                filepath=filepath,
                event_id=fc_response["event_data"]["event_id"],
                uploader_id=fc_response["event_data"]["uploader_id"],
                tenant_id=fc_response["event_data"]["tenant_id"]
            )

            print(data)





        # What's saved on DB until now
        """
        {
            _id: ObjectId('623040aef801ad2c4bb176bd'),
            filename_validation_updated_at: '2022-03-15T07:30:54.152860',
            filename_validation: [
                {
                    message: 'Filename is valid',
                    status: 'success',
                    filename: 'cpuq.txt'
                }
            ],
            updated_at: '2022-03-15T07:30:54.176573',
            app_id: 'app',
            tenant_id: 'b37761e3-6926-4cc1-88c7-4d0478b04adf',
            event_id: 'ce9c7316-912f-4e48-a7a5-a5e34f46f586',
            uploader_id: 'universal_uploader',
            file_content_validation: [
                {
                    message: 'Filename is valid',
                    status: 'success',
                    filename: 'cpuq.txt',
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt'
                }
            ],
            file_content_validation_updated_at: '2022-03-15T07:30:54.168721',
            files_uploaded: [
                '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf_ce9c7316-912f-4e48-a7a5-a5e34f46f586_2022-04-14/cpuq.txt'
            ],
            processing_details: [
                {
                    traceback: null,
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
                    updated_at: '2022-03-15T07:30:54.176577',
                    status: 'success',
                    error: null,
                    step: 'Getting some data out of provided cpuq.txt file',
                    source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py',
                    callable: 'processing_function',
                    success: null
                }
            ]
        }
        """






