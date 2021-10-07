from .register_app import register_app
from .register_uploader import register_uploader
from .register_report import register_report
from .register_component import register_component


#TODO remove this if single requests works
def register_all_multiple_requests(app:dict, reports:list, report_components:list, uploaders:list):
    
    registering_successful = True
    
    _, status_code = register_app(**app)
    if status_code != 200: registering_successful = False
    
    for report in reports:
        _, status_code = register_report(**report)
        if status_code != 200: registering_successful = False
    
    # TODO update registry service
    # for rep_component in report_components:
    #     _, status_code = register_component(**rep_component)
    #     if status_code != 200: registering_successful = False
        
    for uploader in uploaders:
        _, status_code = register_uploader(**uploader)
        if status_code != 200: registering_successful = False
    
    
    if registering_successful:
        return {'status': 'success', 'message': 'Registering process was successful'}, 200
    
    return {'status': 'fail', 'message': 'Registering process was unsuccessful'}, 500
    
    