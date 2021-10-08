from .register_app import register_app
from .register_uploader import register_uploader
from .register_report import register_report
from .register_component import register_component

from licenseware.decorators.auth_decorators import authenticated_machine

#TODO remove this if single requests works
@authenticated_machine
def register_all_multiple_requests(app:dict, reports:list, report_components:list, uploaders:list):
    
    registering_status = True
    
    _, status_code = register_app(**app)
    if status_code != 200: registering_status = False
    
    for report in reports:
        _, status_code = register_report(**report)
        if status_code != 200: registering_status = False
    
    # TODO update registry service
    # for rep_component in report_components:
    #     _, status_code = register_component(**rep_component)
    #     if status_code != 200: registering_status = False
        
    for uploader in uploaders:
        _, status_code = register_uploader(**uploader)
        if status_code != 200: registering_status = False
    
    
    return registering_status
        
    