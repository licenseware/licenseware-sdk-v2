import os
import unittest
import traceback
import uuid

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

        @history.log()
        def processing_function(filepath, event_id, uploader_id, tenant_id):
            """ Getting some data out of provided cpuq.txt file """
            print(f"Processing {filepath}...")
            print("Done!")
            return {"k": "v"}

        for filepath in fc_response["event_data"]["filepaths"]:
            data = processing_function(
                filepath=filepath,
                event_id=fc_response["event_data"]["event_id"],
                uploader_id=fc_response["event_data"]["uploader_id"],
                tenant_id=fc_response["event_data"]["tenant_id"]
            )

            print(data)

        def processing_function_without_decorator(filepath, event_id, uploader_id, tenant_id):
            """ Getting some data out of provided cpuq.txt file """
            print(f"Processing {filepath}...")

            history.add_entities(event_id, entities=[str(uuid.uuid4()), str(uuid.uuid4())])
            # do something else
            history.add_entities(event_id, entities=[str(uuid.uuid4()), str(uuid.uuid4())])

            history.log_success(
                func=processing_function_without_decorator,  # for classes use self.func
                tenant_id=tenant_id,
                event_id=event_id,
                uploader_id=uploader_id,
                filepath=filepath,
                on_success_save="Entities added successfully"
            )

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


        class ProcessingClass:

            def __init__(self, event):
                self.event_id = event["event_data"]["event_id"]
                self.uploader_id = event["event_data"]["uploader_id"]
                self.tenant_id = event["event_data"]["tenant_id"]

            @history.log(on_failure_return={})
            def proc_func_within_class(self, filepath):
                print(f"Processing {filepath}...")
                raise Exception("Something bad happened")
                print("Done!")
                return {"k": "v"}

        pc = ProcessingClass(event=fc_response)

        for filepath in fc_response["event_data"]["filepaths"]:
            data = pc.proc_func_within_class(filepath=filepath)
            print("Result:", data)

        # What's saved on DB until now
        """
        {
            _id: ObjectId('62305cc90fa221d09199e54f'),
            event_id: 'e3a491a2-a2fd-4067-b0c5-1e19ea282c4d',
            app_id: 'app',
            uploader_id: 'universal_uploader',
            updated_at: '2022-03-15T09:30:49.712193',
            filename_validation_updated_at: '2022-03-15T09:30:49.652564',
            tenant_id: 'b37761e3-6926-4cc1-88c7-4d0478b04adf',
            filename_validation: [
                {
                    message: 'Filename is valid',
                    filename: 'cpuq.txt',
                    status: 'success'
                }
            ],
            file_content_validation: [
                {
                    message: 'Filename is valid',
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
                    filename: 'cpuq.txt',
                    status: 'success'
                }
            ],
            file_content_validation_updated_at: '2022-03-15T09:30:49.668121',
            files_uploaded: [
                '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf_e3a491a2-a2fd-4067-b0c5-1e19ea282c4d_2022-04-14/cpuq.txt'
            ],
            processing_details: [
                {
                    success: null,
                    traceback: null,
                    updated_at: '2022-03-15T09:30:49.675298',
                    step: 'Getting some data out of provided cpuq.txt file',
                    error: null,
                    callable: 'processing_function',
                    status: 'success',
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
                    source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py'
                },
                {
                    success: 'Entities added successfully',
                    traceback: null,
                    updated_at: '2022-03-15T09:30:49.696379',
                    step: ' Getting some data out of provided cpuq.txt file ',
                    error: null,
                    callable: 'processing_function_without_decorator',
                    status: 'success',
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
                    source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py'
                },
                {
                    success: null,
                    traceback: 'Traceback (most recent call last):\n  File "/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py", line 183, in processing_function_without_decorator\n    raise Exception("Something bad happened")\nException: Something bad happened\n',
                    updated_at: '2022-03-15T09:30:49.704058',
                    step: ' Getting some data out of provided cpuq.txt file ',
                    error: 'Something bad happened',
                    callable: 'processing_function_without_decorator',
                    status: 'failed',
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
                    source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py'
                },
                {
                    success: null,
                    traceback: 'Traceback (most recent call last):\n  File "/home/acmt/Documents/lware/licenseware-sdk-v2/licenseware/history/history.py", line 229, in wrapper\n    response = f(*args, **kwargs)\n  File "/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py", line 219, in proc_func_within_class\n    raise Exception("Something bad happened")\nException: Something bad happened\n',
                    updated_at: '2022-03-15T09:30:49.712198',
                    step: 'proc_func_within_class',
                    error: 'Something bad happened',
                    callable: 'proc_func_within_class',
                    status: 'failed',
                    filepath: '/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt',
                    source: '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py'
                }
            ],
            entities: [
                '56c6c8e7-7fcb-42eb-b52b-7c9b03f9e9ad',
                '272bf824-5e18-48f8-8cd7-cba6b9c84429',
                '7f2381b7-6e58-4475-820a-39aea8d4602f',
                '426fc6e0-47e7-406c-964e-a41e0ce07ff7'
            ]
        }
        """






