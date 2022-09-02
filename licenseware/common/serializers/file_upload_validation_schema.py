from marshmallow import Schema, fields, validate

from licenseware.common.constants import states


class FileValidationSchema(Schema):
    filename = fields.Str(required=True, validate=validate.Length(min=5))
    status = fields.Str(
        required=True, validate=validate.OneOf(states.SUCCESS, states.FAILED)
    )
    message = fields.Str(required=True, validate=validate.Length(min=10))


class FileUploadValidationSchema(Schema):
    status = fields.Str(
        required=True, validate=validate.OneOf(states.SUCCESS, states.FAILED)
    )
    message = fields.Str(required=True, validate=validate.Length(min=10))
    validation = fields.List(
        fields.Nested(FileValidationSchema), required=False, allow_none=True
    )
    units = fields.Int(requred=False, allow_none=True)
