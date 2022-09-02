from licenseware.common.serializers.integration_details_schema import (
    IntegrationDetailsSchema,
)

from .schema_validator import schema_validator


def validate_integration_details(data: dict, raise_error=True):
    return schema_validator(IntegrationDetailsSchema, data, raise_error=raise_error)
