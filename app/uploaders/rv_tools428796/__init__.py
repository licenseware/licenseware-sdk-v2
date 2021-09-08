from .worker import rv_tools428796_worker
from .validator import rv_tools428796_validator

from licenseware.uploader_builder import UploaderBuilder


rv_tools428796_uploader = UploaderBuilder(
    name="Set uploader name here", 
    uploader_id = "rv_tools428796",
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools428796_validator,
    worker_function=rv_tools428796_worker,
    quota_units = 1
)