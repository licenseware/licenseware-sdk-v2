from .worker import rv_tools854322_worker
from .validator import rv_tools854322_validator

from licenseware.uploader_builder import UploaderBuilder


rv_tools854322_uploader = UploaderBuilder(
    name="RvTools854322", 
    uploader_id = "rv_tools854322",
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools854322_validator,
    worker_function=rv_tools854322_worker,
    quota_units = 1
)