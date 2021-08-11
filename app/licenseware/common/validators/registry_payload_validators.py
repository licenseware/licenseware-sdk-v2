from app.licenseware.utils.logger import log
from app.licenseware.common.serializers import RegisterAppPayloadSchema
from app.licenseware.common.serializers import RegisterUploaderPayloadSchema

from .schema_validator import schema_validator



def validate_register_app_payload(payload:dict, raise_error=True):
    schema_validator(RegisterAppPayloadSchema, payload, raise_error=raise_error)
    
    
def validate_register_uploader_payload(payload:dict, raise_error=True):
    schema_validator(RegisterUploaderPayloadSchema, payload, raise_error=raise_error)
    
