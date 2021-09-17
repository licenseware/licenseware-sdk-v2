from .worker import rv_tools723908_worker
from .validator import rv_tools723908_validator

from licenseware.uploader_builder import UploaderBuilder


rv_tools723908_uploader = UploaderBuilder(
    name="RvTools723908", 
    uploader_id = "rv_tools723908",
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools723908_validator,
    worker_function=rv_tools723908_worker,
    quota_units = 1
)