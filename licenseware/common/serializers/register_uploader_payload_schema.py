from marshmallow import validate  # utils validatiors
from marshmallow import Schema, fields

from licenseware.common.constants import flags, states
from licenseware.common.validators.validate_icon import validate_icon


class FileValidatorSchema(Schema):
    filename_contains = fields.List(fields.Str, required=False, allow_none=True)
    filename_endswith = fields.List(fields.Str, required=False, allow_none=True)
    ignore_filenames = fields.List(fields.Str, required=False, allow_none=True)
    required_input_type = fields.Str(required=False, allow_none=True)
    required_sheets = fields.List(fields.Str, required=False, allow_none=True)
    required_columns = fields.List(fields.Str, required=False, allow_none=True)
    text_contains_all = fields.List(fields.Str, required=False, allow_none=True)
    text_contains_any = fields.List(fields.Str, required=False, allow_none=True)
    min_rows_number = fields.Int(required=False, allow_none=True)
    header_starts_at = fields.Int(required=False, allow_none=True)
    buffer = fields.Int(required=False, allow_none=True)
    filename_valid_message = fields.Str(required=False, allow_none=True)
    filename_invalid_message = fields.Str(required=False, allow_none=True)
    filename_ignored_message = fields.Str(required=False, allow_none=True)


class UploaderInfoSchema(Schema):

    app_id = fields.Str(required=True, validate=validate.Length(min=3))
    uploader_id = fields.Str(required=True, validate=validate.Length(min=3))
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    flags = fields.List(
        fields.Str,
        required=False,
        validate=validate.OneOf([None, flags.BETA, flags.SOON]),
        allow_none=True,
    )
    accepted_file_types = fields.List(fields.Str, required=True)
    upload_url = fields.Url(required=True)
    upload_validation_url = fields.Url(required=True)
    quota_validation_url = fields.Url(required=True)
    status_check_url = fields.Url(required=True)
    icon = fields.Str(required=False, validate=validate_icon)
    status = fields.Str(
        required=False,
        validate=validate.OneOf([None, states.IDLE, states.RUNNING]),
        allow_none=True,
    )
    validation_parameters = fields.Nested(FileValidatorSchema, required=True)


class RegisterUploaderPayloadSchema(Schema):
    data = fields.List(fields.Nested(UploaderInfoSchema), required=True)
