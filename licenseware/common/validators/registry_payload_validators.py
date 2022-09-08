from licenseware.common.serializers import (
    RegisterAppPayloadSchema,
    RegisterReportComponentPayloadSchema,
    RegisterReportPayloadSchema,
    RegisterUploaderPayloadSchema,
    RegisterUploaderStatusPayloadSchema,
)
from licenseware.common.validators.schema_validator import schema_validator


def validate_register_app_payload(payload: dict, raise_error=True):
    return schema_validator(RegisterAppPayloadSchema, payload, raise_error=raise_error)


def validate_register_uploader_payload(payload: dict, raise_error=True):
    return schema_validator(
        RegisterUploaderPayloadSchema, payload, raise_error=raise_error
    )


def validate_register_uploader_status_payload(payload: dict, raise_error=True):
    return schema_validator(
        RegisterUploaderStatusPayloadSchema, payload, raise_error=raise_error
    )


def validate_register_report_payload(payload: dict, raise_error=True):
    return schema_validator(
        RegisterReportPayloadSchema, payload, raise_error=raise_error
    )


def validate_register_report_component_payload(payload: dict, raise_error=True):
    return schema_validator(
        RegisterReportComponentPayloadSchema, payload, raise_error=raise_error
    )
