import os
from typing import Tuple

import requests
from flask import Request

from licenseware.common.constants.envs import envs
from licenseware.common.constants.states import states
from licenseware.quota import Quota
from licenseware.uploader_validator.file_content_validator import FileContentValidator
from licenseware.uploader_validator.filename_validator import FileNameValidator
from licenseware.utils.logger import log


class UploaderValidator(FileNameValidator, FileContentValidator):

    """ """

    def __init__(
        self,
        filename_contains: list = [],
        filename_endswith: list = [],
        ignore_filenames: list = [],
        required_input_type: str = None,
        required_sheets: list = [],
        required_columns: list = [],
        text_contains_all: list = [],
        text_contains_any: list = [],
        regex_escape: bool = True,
        min_rows_number: int = 0,
        header_starts_at: int = 0,
        buffer: int = 9000,
        filename_valid_message="File is valid",
        filename_invalid_message=None,
        filename_ignored_message="File is ignored",
        ignored_by_uup: bool = False,  # ignored from universal uploader matcher
        _uploader_id: str = None,
        _quota_units: int = None,
        **options,
    ):
        self.quota_units = _quota_units
        self.uploader_id = _uploader_id
        self.filename_contains = filename_contains
        self.filename_endswith = filename_endswith
        self.ignore_filenames = ignore_filenames
        self.required_input_type = required_input_type
        self.required_sheets = required_sheets
        self.required_columns = required_columns
        self.text_contains_all = text_contains_all
        self.text_contains_any = text_contains_any
        self.regex_escape = regex_escape
        self.min_rows_number = min_rows_number
        self.header_starts_at = header_starts_at
        self.buffer = buffer
        self.filename_valid_message = filename_valid_message
        self.filename_invalid_message = filename_invalid_message
        self.filename_ignored_message = filename_ignored_message
        self.ignored_by_uup = ignored_by_uup
        self.options = options
        self.validation_parameters = self.get_validation_parameters()
        super().__init__(**vars(self))

    def quota_within_limits(
        self, tenant_id: str, auth_token: str, units: int
    ) -> Tuple[dict, int]:

        q = Quota(
            tenant_id=tenant_id,
            auth_token=auth_token,
            uploader_id=self.uploader_id,
            units=self.quota_units,
        )

        response, status_code = q.check_quota(units)

        return response, status_code

    def update_quota(
        self, tenant_id: str, auth_token: str, units: int
    ) -> Tuple[dict, int]:

        q = Quota(
            tenant_id=tenant_id,
            auth_token=auth_token,
            uploader_id=self.uploader_id,
            units=self.quota_units,
        )

        response, status_code = q.update_quota(units)

        return response, status_code

    def calculate_quota(
        self, flask_request: Request, update_quota_units: bool = True
    ) -> Tuple[dict, int]:

        if self.quota_units is None:
            return {
                "status": states.SUCCESS,
                "message": "Quota is skipped quota units is null",
            }, 200

        tenant_id = flask_request.headers.get("Tenantid")
        auth_token = flask_request.headers.get("Authorization")

        response = requests.get(
            url=envs.AUTH_MACHINE_CHECK_URL, headers={"Authorization": auth_token}
        )
        if response.status_code == 200:
            return {
                "status": states.SUCCESS,
                "message": "Quota is skipped request from a machine",
            }, 200

        log.warning("Calculating quota based on length of files")

        file_objects = flask_request.files.getlist("files[]")

        current_units_to_process = len(file_objects)

        quota_check_response, quota_check_status = self.quota_within_limits(
            tenant_id, auth_token, current_units_to_process
        )

        log.info(quota_check_response)

        if quota_check_status == 200 and update_quota_units == True:
            response, status_code = self.update_quota(
                tenant_id, auth_token, current_units_to_process
            )

            log.info(response)

        return quota_check_response, quota_check_status

    @classmethod
    def get_filepaths_from_objects_response(cls, file_objects_response):

        file_paths = [res["filepath"] for res in file_objects_response["validation"]]

        return file_paths

    @classmethod
    def get_only_valid_filepaths_from_objects_response(cls, file_objects_response):

        file_paths = [
            res["filepath"]
            for res in file_objects_response["validation"]
            if res["filepath"] != "File not saved" and os.path.exists(res["filepath"])
        ]

        return file_paths

    def get_validation_parameters(self):

        return dict(
            filename_contains=self.filename_contains,
            filename_endswith=self.filename_endswith,
            ignore_filenames=self.ignore_filenames,
            required_input_type=self.required_input_type,
            required_sheets=self.required_sheets,
            required_columns=self.required_columns,
            text_contains_all=self.text_contains_all,
            text_contains_any=self.text_contains_any,
            min_rows_number=self.min_rows_number,
            header_starts_at=self.header_starts_at,
            buffer=self.buffer,
            filename_valid_message=self.filename_valid_message,
            filename_invalid_message=self.filename_invalid_message,
            filename_ignored_message=self.filename_ignored_message,
            regex_escape=self.regex_escape,
            ignored_by_uup=self.ignored_by_uup,
        )

    def get_full_validation_response(self, filepath: str):

        filename = os.path.basename(filepath)
        filename_validation_response = self.validate_filenames([filename])
        file_name_ok = filename_validation_response[0]["status"] == states.SUCCESS
        file_response = filename_validation_response[0]["message"]

        content_validation_response = self.validate_filepaths_content([filepath])
        log.info(content_validation_response)
        file_content_ok = content_validation_response[0]["status"] == states.SUCCESS
        content_response = content_validation_response[0]["message"]

        log.info(
            f"{filename} - file_name_ok:{file_name_ok}, file_content_ok:{file_content_ok}"
        )
        log.info(f"{self.uploader_id} - {all([file_name_ok, file_content_ok])}")

        fileok = all([file_name_ok, file_content_ok])

        message = f"{'Name: ' + file_response if not file_name_ok else ''}{' Content: ' + content_response if not file_content_ok else ''}".strip()

        return {
            "status": states.SUCCESS if fileok else states.SKIPPED,
            "name": file_name_ok,
            "content": file_content_ok,
            "message": message or "File is valid",
        }

    def valid_filepath(self, filepath: str):

        filename = os.path.basename(filepath)
        filename_validation_response = self.validate_filenames([filename])
        file_name_ok = filename_validation_response[0]["status"] == states.SUCCESS

        file_content_ok = False
        if file_name_ok:
            content_validation_response = self.validate_filepaths_content([filepath])
            log.info(content_validation_response)
            file_content_ok = content_validation_response[0]["status"] == states.SUCCESS

        log.info(
            f"{filename} - file_name_ok:{file_name_ok}, file_content_ok:{file_content_ok}"
        )
        log.info(f"{self.uploader_id} - {all([file_name_ok, file_content_ok])}")

        return all([file_name_ok, file_content_ok])
