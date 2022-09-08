from licenseware.common.serializers.event_schema import EventSchema
from licenseware.common.validators.schema_validator import schema_validator


def validate_event(payload: dict, raise_error=True):
    return schema_validator(EventSchema, payload, raise_error=raise_error)
