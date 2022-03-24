from .worker import {{ uploader_id }}_worker
from .validator import {{ uploader_id }}_validator

from licenseware.uploader_builder import UploaderBuilder


{{ uploader_id }}_uploader = UploaderBuilder(
    name="{{ uploader_id.split('_') | map('title') | join('') }}", 
    uploader_id = "{{ uploader_id }}",
    description="Set uploader description", 
    accepted_file_types=['.xls', '.xlsx'],
    validator_class={{ uploader_id }}_validator,
    worker_function={{ uploader_id }}_worker,
    quota_units = 1
)
