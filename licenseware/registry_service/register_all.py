from licenseware.utils.logger import log
from licenseware.decorators.auth_decorators import authenticated_machine

from .register_all_multiple_requests import register_all_multiple_requests
from .register_all_single_requests import register_all_single_requests




@authenticated_machine
def register_all(
    app:dict, 
    reports:list, 
    report_components:list, 
    uploaders:list, 
    single_request:bool = False
):
    
    if single_request: 
        return register_all_single_requests(app, reports, report_components, uploaders)
    
    return register_all_multiple_requests(app, reports, report_components, uploaders)
    