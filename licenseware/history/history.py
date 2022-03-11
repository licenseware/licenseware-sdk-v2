"""
Specs:

[X] create an event_id for the file(s) uploaded
    - the event_id is a unique uuid4 id which allows us to track the files uploaded in the processing pipeline
    Resolution:
    When the `validate_filenames` function from `UploaderBuilder` sdk class is called,
    parameters `EventId` and `UploaderId` are added on the headers.
    On the next step when files are sent for upload and the file content validation is triggered
    the `EventId` and `UploaderId` will be taken from the headers received from frontend (`UploaderId` is optional).

[] save each response from the validation steps
    - save filename validation response
    - save file content validation response
    - save files uploaded on disk under a tenant_id/event_id folder (files saved will be useful in reproducing the error)
    - delete files saved in /event_id folder if the processing was successful (0 errors) to avoid filling the disk

[] allow logging history and return an alternate response in case of failure
    - adding `History.log()` decorator on processing functions will save the raised errors in db
    and return an alternate `empty` response (either an empty dict/list
    or None which can be handled in the next step of the processing pipeline)
    - `History.log()` decorator requires one job for each function with raise error where needed
    - also allow using where not possible (big funcs which do a lot of things) logging/saving error/success responses
    `History.log_entities(**data)`, `History.log_success(**data)` and `History.log_failure(**data)` functions can be used

[] different history stats schema based on the type of files processed
    - currently there are 2 types of processed files
        1. files that are processed in bulk (the processing pipeline requires uploading more than 1 file)
        2. files that are processed one by one (the processing pipeline requires uploading just 1 file)
        3. single file with multiple entities?TODO


Entities:
 - devices
 - databases
 - products
 - list can be expanded

Test on: ODB (review_lite, lms_options)

review_lite - databases from filename
lms_options - databases from content

save db ids (uuid4) to entities_ids

HistoryStatsSchema (for files processed one by one):

{
    "tenant_id": "xxx",
    "event_id": "xxxx",
    "uploader_id": "rv_lite",
    "entities_ids": [
        "uuid4 strings"
    ],
    "filename_validation": [
        {"file_path": "/path/file", "response": the filename validation response},
        etc
    ],
    "file_content_validationr bulk file should look:": [
        {"file_path": "/path/file", "response": the file content validation response},
        etc
    ],
    "files_uploaded": [file_path1, file_path2, file_path3],
    "processing_details": [
            {
                "step": "Getting machines CPU cores",
                "error": "Value in column x not an integer",
                "processed_file_path": "path/to/file/processed",
                "traceback": "traceback error"
            }
            etc
    ]
}


def procFunc():
    ''' processing xxx '''
    raise Exception("X not found in y")


HistoryStatsSchema (for files processed in bulk):
Files processed in bulk are grouped in list

{
    "tenant_id": "xxx",
    "event_id": "xxxx",
    "uploader_id": "rv_lite",
    "filename_validation": [
        [
            {"file_path": "/path/file", "response": the filename validation response},
            etc
        ]
    ],
    "file_content_validation": [
        [
            {"file_path": "/path/file", "response": the file content validation response},
            etc
        ]
    ],
    "files_uploaded": [[file_path1, file_path2, file_path3], etc],
    "processing_details": [
            [
                {
                "step": "Getting machines CPU cores",
                "error": "Value in column x not an integer",
                "processed_file_path": "path/to/file/processed",
                "traceback": "traceback error"
                }
                etc
            ]
    ]
}

"""
import uuid
from functools import wraps
from licenseware import mongodata
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.common.serializers import WildSchema
from .metadata import get_metadata, append_headers_on_validation_funcs


class History:

    @staticmethod
    def save_step(metadata):
        return mongodata.insert(
            schema=WildSchema,
            data=metadata,
            collection=envs.MONGO_COLLECTION_HISTORY_NAME
        )

    @staticmethod
    def log(*dargs, success_message=None, failed_message=None):
        def _decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                try:
                    # Handle case where files are uploaded and EventId is not provided in the headers
                    if f.__name__ == 'upload_files' and args[0].headers.get("EventId") is None:
                        kwargs.update({"event_id": str(uuid.uuid4())})

                    response = f(*args, **kwargs)
                    metadata = get_metadata(f, args, kwargs)
                    response = append_headers_on_validation_funcs(metadata, response)
                    if success_message: log.success(success_message)
                    return response

                except Exception as err:

                    log.exception(err)
                    if failed_message: log.error(failed_message)
                    else: log.error(err)

                    raise err

            return wrapper

        return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
