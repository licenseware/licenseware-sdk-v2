from .worker import rv_tools524833_worker
from .validator import rv_tools524833_validator

from licenseware.uploader_builder import UploaderBuilder


rv_tools524833_uploader = UploaderBuilder(
    name="RvTools524833", 
    uploader_id = "rv_tools524833",
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools524833_validator,
    worker_function=rv_tools524833_worker,
    quota_units = 1
)