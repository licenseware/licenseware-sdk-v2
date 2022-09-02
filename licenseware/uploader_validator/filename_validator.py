from typing import List

from licenseware.common.constants import states
from licenseware.common.validators.file_validators import validate_filename


class FileNameValidator:

    """
    This class is reponsible for validating filenames
    """

    def __init__(
        self,
        uploader_id: str,
        ignore_filenames: list = [],
        filename_contains: list = [],
        filename_endswith: list = [],
        filename_valid_message: str = "Filename is valid",
        filename_invalid_message: str = None,
        filename_ignored_message: str = "Filename is ignored",
        regex_escape: bool = True,
        **kwargs
    ):
        self.uploader_id = uploader_id
        self.ignore_filenames = ignore_filenames
        self.filename_contains = filename_contains
        self.filename_endswith = filename_endswith
        self.filename_valid_message = filename_valid_message
        self.filename_invalid_message = filename_invalid_message
        self.filename_ignored_message = filename_ignored_message
        self.regex_escape = regex_escape
        # prevents overflow of params allows extending with non-default parameters
        self.kwargs = kwargs

    def get_filenames_from_request(self, flask_request):
        """
        validate request received
        filename validation request should be a list of filenames
        """

        filenames = flask_request.json

        bad_request = {
            "status": states.FAILED,
            "message": "Filenames sent for validation must be in a list of strings format",
        }, 400

        if filenames == None:
            return bad_request
        if isinstance(filenames, str):
            return bad_request

        if isinstance(filenames, list):
            if len(filenames) == 0:
                return bad_request

        if isinstance(filenames, dict):
            if "filenames" not in filenames:
                return bad_request
            if len(filenames["filenames"]) == 0:
                return bad_request
            filenames = filenames["filenames"]

        return filenames

    def validate_filenames(self, filenames: List[str]) -> List[dict]:
        """
        receive a list of filenames and validate them based on
        `filename_contains` and `filename_endswith` input parameters
        return a list of dicts with validation status, filename and message

        it's recomented to leave `filename_invalid_message` paramters as is
        because if None will provide the reason why filename validation failed
        """

        validation_response = []
        for filename in filenames:

            if any(filename.endswith(f) for f in self.ignore_filenames):

                validation_response.append(
                    {
                        "status": states.SKIPPED,
                        "filename": filename,
                        "message": self.filename_ignored_message,
                    }
                )

                continue

            try:
                validate_filename(
                    filename,
                    contains=self.filename_contains,
                    endswith=self.filename_endswith,
                    regex_escape=self.regex_escape,
                )
                validation_response.append(
                    {
                        "status": states.SUCCESS,
                        "filename": filename,
                        "message": self.filename_valid_message,
                    }
                )
            except Exception as err:
                validation_response.append(
                    {
                        "status": states.FAILED,
                        "filename": filename,
                        "message": self.filename_invalid_message or str(err),
                    }
                )

        return validation_response

    def get_filenames_response(self, flask_request):
        """
        receive flask_request
        validate filenames
        create json response
        """

        filenames = self.get_filenames_from_request(flask_request)
        if isinstance(filenames, tuple):
            return filenames
        validation_response = self.validate_filenames(filenames)

        return {
            "status": states.SUCCESS,
            "message": "Filenames are valid",
            "validation": validation_response,
        }, 200
