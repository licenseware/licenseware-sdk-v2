from .worker import rv_tools_worker
from .validator import rv_tools_validator

from licenseware.uploader_builder import UploaderBuilder


rv_tools_uploader = UploaderBuilder(
    name="Set uploader name here", 
    uploader_id = 'rv_tools',
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class=rv_tools_validator,
    worker_function=rv_tools_worker,
    quota_units = 1
)
