from .worker import rv_tools491412_worker
from .validator import rv_tools491412_validator

from licenseware.uploader_builder import UploaderBuilder


rv_tools491412_uploader = UploaderBuilder(
    name="RvTools491412", 
    uploader_id = "rv_tools491412",
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools491412_validator,
    worker_function=rv_tools491412_worker,
    quota_units = 1
)