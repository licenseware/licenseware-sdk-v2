"""
Specs:

[X] create an event_id for the file(s) uploaded
    - the event_id is a unique uuid4 id which allows us to track the files uploaded in the processing pipeline
    Resolution:
    When the `validate_filenames` function from `UploaderBuilder` sdk class is called,
    parameters `EventId` and `UploaderId` are added on the headers.
    On the next step when files are sent for upload and the file content validation is triggered
    the `EventId` and `UploaderId` will be taken from the headers received from frontend (`UploaderId` is optional).

[X] save each response from the validation steps
    - save filename validation response
    - save file content validation response
    - save files uploaded on disk under a tenant_id_event_id_delete_date folder (files saved will be useful in reproducing the error)
    - delete files saved in /event_id folder by a cron job

[X] allow logging history and return an alternate response in case of failure
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
import inspect
import traceback
from functools import wraps
from pymongo.collection import Collection
from licenseware import mongodata
from licenseware.mongodata import collection
from licenseware.common.serializers import WildSchema
from licenseware.common.constants import envs
from licenseware.utils.logger import log as logg
from .metadata import get_metadata, create_metadata, append_headers_on_validation_funcs
from .step import save_step

__all__ = ['add_entities', 'remove_entities', 'log_failure', 'log_success', 'log']


def add_entities(
        event_id: str,
        entities: list = None
):
    return mongodata.update(
        schema=WildSchema,
        match={'event_id': event_id},
        new_data={"entities": entities},
        append=True,
        collection=envs.MONGO_COLLECTION_HISTORY_NAME
    )


def remove_entities(
        event_id: str,
        entities: list = None
):
    with collection(envs.MONGO_COLLECTION_HISTORY_NAME) as col:
        col: Collection
        updated = col.update_one(
            filter={'event_id': event_id},
            update={'$pull': {'entities': {"$in": entities}}}
        ).modified_count

    return updated


def log_success(
        func: callable,
        tenant_id: str,
        event_id: str,
        uploader_id: str,
        filepath: str,
        on_success_save: str = None,
        **overflow
):
    func_name = func.__name__
    step = func.__doc__ or func.__name__
    func_source = str(inspect.getmodule(func)).split("from")[1].strip().replace("'", "").replace(">", "")

    metadata = create_metadata(step, tenant_id, event_id, uploader_id, filepath, func_name, func_source)
    save_step(metadata, None, on_success_save, None)
    return metadata


def log_failure(
        func: callable,
        tenant_id: str,
        event_id: str,
        uploader_id: str,
        filepath: str,
        error_string: str,
        traceback_string: str,
        on_failure_save: str = None,
        **overflow
):

    func_name = func.__name__
    step = func.__doc__ or func.__name__
    func_source = str(inspect.getmodule(func)).split("from")[1].strip().replace("'", "").replace(">", "")

    metadata = create_metadata(step, tenant_id, event_id, uploader_id, filepath, func_name, func_source)
    save_step(metadata, {
        'error': error_string,
        'traceback': traceback_string
    }, None, on_failure_save, True)
    return metadata


def log(*dargs, on_success_save: str = None, on_failure_save: str = None, on_failure_return: any = None):
    """
        param: on_success_save - what to save on history logs if function didn't raised any errors
        param: on_failure_save - what to save on history logs if function raised error
        param: on_failure_return - if function raised an error return this instead (for safe processing)
        If you want on failure to return None put it as a string `on_failure_return="None"`
        Ex:
        ```
            @history.log(on_failure_return={})
            def procFunc(*args, **kwargs):
                raise Exception("Failed")

            >> print(procFunc())
            >> {}
        ```
    """
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"History kwargs: on_success_save:{on_success_save}, on_failure_save:{on_failure_save}, on_failure_return:{on_failure_return}")
            # Handle case where files are uploaded and EventId is not provided in the headers
            if f.__name__ == 'upload_files' and len(args) > 1:
                if hasattr(args[1], "headers"):
                    if args[1].headers.get("EventId") is None:
                        logg.info("EventId not provided from frontend.\nUpdated with `event_id`.")
                        kwargs.update({"event_id": str(uuid.uuid4())})

            metadata = get_metadata(f, args, kwargs)
            try:
                response = f(*args, **kwargs)
                save_step(metadata, response, on_success_save, on_failure_save)
                response = append_headers_on_validation_funcs(metadata, response)
                return response
            except Exception as err:

                save_step(metadata, {
                    'error': str(err),
                    'traceback': str(traceback.format_exc())
                }, on_success_save, on_failure_save, True)

                if on_failure_return is not None:
                    return on_failure_return
                elif on_failure_return == "None":
                    return None
                else:
                    logg.exception(err)
                    raise err

        return wrapper
    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
