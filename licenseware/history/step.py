import datetime
import os
import shutil

from licenseware import mongodata
from licenseware.common.constants import envs, states
from licenseware.history.history_schemas import HistorySchema
from licenseware.utils.logger import log as logg


def save_filename_validation(metadata, response):

    data = {
        "tenant_id": metadata["tenant_id"],
        "event_id": metadata["event_id"],
        "app_id": metadata["app_id"],
        "uploader_id": metadata["uploader_id"],
        "filename_validation": response["validation"],
        "filename_validation_updated_at": datetime.datetime.utcnow().isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return mongodata.insert(
        schema=HistorySchema, data=data, collection=envs.MONGO_COLLECTION_HISTORY_NAME
    )


def copy_files_uploaded_on_event_folder(data):
    """
    Files uploaded are saved in another folder for the purpose of replicating the errors
    Files will be deleted after 1 month (iso date specifies when files will be deleted)
    """
    if envs.DESKTOP_ENVIRONMENT:
        return []

    expiration_iso_date = (
        (datetime.datetime.utcnow() + datetime.timedelta(days=30)).date().isoformat()
    )
    folder_name = f"{data['tenant_id']}_{data['event_id']}_{expiration_iso_date}"
    folder_path = os.path.join(envs.FILE_UPLOAD_PATH, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files_uploaded_on_event = []
    for fp in data["files_uploaded"]:
        save_path = os.path.join(folder_path, os.path.basename(fp))
        shutil.copy2(src=fp, dst=save_path)
        files_uploaded_on_event.append(save_path)

    return files_uploaded_on_event


def save_file_content_validation(metadata, response):

    if "validation" not in response:
        logg.info("Parameter `validation` not found on response from `upload_files`")
        return

    file_content_validation = response["validation"]
    filepaths = [cv["filepath"] for cv in response["validation"]]

    data = {
        "tenant_id": metadata["tenant_id"],
        "event_id": metadata["event_id"],
        "app_id": metadata["app_id"],
        "uploader_id": metadata["uploader_id"],
        "file_content_validation": file_content_validation,
        "files_uploaded": filepaths,
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    # copy_files_uploaded_on_event_folder(data)
    data["files_uploaded"] = ["disabled for now"]
    data["file_content_validation_updated_at"] = datetime.datetime.utcnow().isoformat()

    return mongodata.update(
        schema=HistorySchema,
        match={"tenant_id": metadata["tenant_id"], "event_id": metadata["event_id"]},
        new_data=data,
        collection=envs.MONGO_COLLECTION_HISTORY_NAME,
    )


def save_processing_details(metadata, response):

    data = {
        "tenant_id": metadata["tenant_id"],
        "event_id": metadata["event_id"],
        "app_id": metadata["app_id"],
        "uploader_id": metadata["uploader_id"],
        "updated_at": datetime.datetime.utcnow().isoformat(),
        "processing_details": [
            {
                "step": metadata["step"],
                "filepath": metadata["filepath"],
                "status": response["status"],
                "success": response["success"],
                "error": response["error"],
                "traceback": response["traceback"],
                "callable": metadata["callable"],
                "source": metadata["source"],
                "file_name": metadata["file_name"],
                "updated_at": datetime.datetime.utcnow().isoformat(),
            }
        ],
    }

    return mongodata.update(
        schema=HistorySchema,
        match={"tenant_id": metadata["tenant_id"], "event_id": metadata["event_id"]},
        new_data=data,
        append=True,
        collection=envs.MONGO_COLLECTION_HISTORY_NAME,
    )


def save_step(
    metadata,
    response,
    on_success_save: any = None,
    on_failure_save: any = None,
    raised_error: bool = False,
):
    # We can't track files without an event_id
    if metadata["event_id"] is None:
        return

    if metadata["callable"] == "validate_filenames":
        return save_filename_validation(metadata, response[0])

    if metadata["callable"] == "upload_files":
        return save_file_content_validation(metadata, response[0])

    # Success cases
    if not raised_error and on_success_save:
        return save_processing_details(
            metadata,
            {
                "status": states.SUCCESS,
                "success": on_success_save,
                "error": None,
                "traceback": None,
            },
        )
    if not raised_error and not on_success_save:
        return save_processing_details(
            metadata,
            {
                "status": states.SUCCESS,
                "success": None,
                "error": None,
                "traceback": None,
            },
        )

    # Failed cases
    if raised_error and on_failure_save:
        return save_processing_details(
            metadata,
            {
                "status": states.FAILED,
                "success": None,
                "error": on_failure_save,
                "traceback": response["traceback"],
            },
        )

    if raised_error and not on_failure_save:
        return save_processing_details(
            metadata,
            {
                "status": states.FAILED,
                "success": None,
                "error": response["error"],
                "traceback": response["traceback"],
            },
        )


# File validation response
# {
#   "status": "success",
#   "message": "Filenames are valid",
#   "validation": [
#     {
#       "status": "success",
#       "filename": "rvtools.xlsx",
#       "message": "Filename is valid"
#     },
#     {
#       "status": "success",
#       "filename": "options.csv",
#       "message": "Filename is valid"
#     }
#   ]
# }

# Upload files response
# {
#   "status": "success",
#   "message": "Event sent",
#   "event_data": {
#     "tenant_id": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
#     "uploader_id": "universal_uploader",
#     "filepaths": [
#       "/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt"
#     ],
#     "flask_request": {
#       "Host": "localhost",
#       "Connection": "keep-alive",
#       "X-Forwarded-For": "172.18.0.1",
#       "X-Forwarded-Proto": "http",
#       "X-Forwarded-Host": "localhost",
#       "X-Forwarded-Port": "80",
#       "X-Forwarded-Path": "/universal-uploader/uploads/universal_uploader/files",
#       "X-Real-Ip": "172.18.0.1",
#       "Content-Length": "6655",
#       "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
#       "Sec-Ch-Ua-Mobile": "?0",
#       "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDczMjg4MzAsImlhdCI6MTY0NzI0MjQyNSwic3ViIjoiMzc0MmQ4ODgtNzNjNS00MTA1LTk4OTgtYjIwZjZhMmNlMjM1In0.3IrFRs4-VQiYzUCTc_QgZKQo8NVnbdSmRWmU4s7eRfE",
#       "Tenantid": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
#       "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryFy5k1hbwcuEa1dsf",
#       "Accept": "application/json",
#       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
#       "Sec-Ch-Ua-Platform": "\"Linux\"",
#       "Origin": "http://localhost",
#       "Sec-Fetch-Site": "same-origin",
#       "Sec-Fetch-Mode": "cors",
#       "Sec-Fetch-Dest": "empty",
#       "Referer": "http://localhost/universal-uploader/docs",
#       "Accept-Encoding": "gzip, deflate, br",
#       "Accept-Language": "en-US,en;q=0.9,ro;q=0.8,it;q=0.7,fr;q=0.6",
#       "Cookie": "PGADMIN_LANGUAGE=en; username-localhost-8889=\"2|1:0|10:1646133817|23:username-localhost-8889|44:ZTZkMjJhN2NkZWM2NDNmZDkxYTVkNTVjYTg0NjRlM2E=|38b7f9e169bfa62662aa3ff1d146050f2964b793dc3902120ba90c4e20535626\"; username-localhost-8888=\"2|1:0|10:1646996386|23:username-localhost-8888|44:MmQzODg2ODhjY2E0NDY1Yzg1Y2FhOWUwY2EzYjRlZDY=|e72eb76bbecc87382940894602d81bb601977e231173ac0d2922d8fc4b1218b4\"; _xsrf=2|3ea9ea76|6ebac8ec76a4cd27fed85d0eb847f7bd|1646996386; mongo-express=s%3AVAettPkb_tNq0EZQcZqY96UKMb4vQ_s1.m02RdaZSFY5qVSrgPU%2FkfwHsrhojQX0P8gGOnjMZ1Ys"
#     },
#     "validation_response": {
#       "tenant_id": "b37761e3-6926-4cc1-88c7-4d0478b04adf",
#       "status": "success",
#       "message": "Files are valid",
#       "validation": [
#         {
#           "status": "success",
#           "filename": "cpuq.txt",
#           "filepath": "/tmp/lware/b37761e3-6926-4cc1-88c7-4d0478b04adf/cpuq.txt",
#           "message": "Filename is valid"
#         }
#       ]
#     }
#   }
# }


# {
#     'callable': 'validate_filenames_no_flask_request',
#     'docs': 'Validate filenames received', 'source':
#     '/home/acmt/Documents/lware/licenseware-sdk-v2/tests/test_history.py',
#     'tenant_id': '123',
#     'event_id': 'wer',
#     'app_id': 'app',
#     'uploader_id': 'rv_tools'
# }


# {
#     "tenant_id": "xxx",
#     "event_id": "xxxx",
#     "app_id": "",
#     "uploader_id": "rv_lite",
#     "entities_ids": [
#         "uuid4 strings"
#     ],
#     "filename_validation": [
#         {"file_path": "/path/file", "response": the filename validation response},
#         etc
#     ],
#     "file_content_validatio nr bulk file should look:": [
#         {"file_path": "/path/file", "response": the file content validation response},
#         etc
#     ],
#     "files_uploaded": [file_path1, file_path2, file_path3],
#     "processing_details": [
#             {
#                 "step": "Getting machines CPU cores",
#                 "error": "Value in column x not an integer",
#                 "processed_file_path": "path/to/file/processed",
#                 "traceback": "traceback error"
#             }
#             etc
#     ]
# }
