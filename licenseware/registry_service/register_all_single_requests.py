from typing import Callable
import requests
from licenseware.utils.logger import log
from licenseware.common.constants import envs

from .register_app import register_app
from .register_uploader import register_uploader
from .register_report import register_report
from .register_component import register_component
    

    
def _register_with_single_request(registrable_name:str, registrable_func:Callable, registrable_list:list):
       
    registry_url, auth_headers = None, None
    post_data_list = []
    for registrable in registrable_list:
        post_data = registrable_func(get_kwargs=True, **registrable)
        if isinstance(post_data, tuple): continue
        post_data_list.append(post_data)
        
        if not registry_url:
            registry_url, auth_headers = post_data['url'], post_data['headers']
        
        
    payload = {'data': []}
    for post_data in post_data_list:
        payload['data'].extend(post_data['json']['data'])
   
    if not payload['data']: return {
        "status": "success",
        "message": f"{registrable_name.capitalize()} not provided",
        "content": payload
    }, 200

    
    log.info(f"Registering {registrable_name}...")
    # log.info(payload)
    registration = requests.post(url=registry_url, json=payload, headers=auth_headers)
    
    if registration.status_code != 200:    
        nokmsg = f"Could not register {registrable_name}"
        log.error(nokmsg)
        return { "status": "fail", "message": nokmsg, "content": payload }, 500
    
    
    log.info(f"Registering {registrable_name} successfull!")
    
    return {
        "status": "success",
        "message": f"{registrable_name.capitalize()} registered successfully",
        "content": payload
    }, 200

    
    
    
def register_all_single_requests(app:dict, reports:list, report_components:list, uploaders:list):
    
    registering_status = True
    
    log.info(f"Registering '{envs.APP_ID}' app...")
    
    _, status_code = register_app(**app)
    if status_code != 200: registering_status = False
    
    log.info(f"Registering '{envs.APP_ID}' app successfull!")
    
    
    _, status_code = _register_with_single_request(
        registrable_name='reports', 
        registrable_func=register_report, 
        registrable_list=reports
    )
    if status_code != 200: registering_status = False
    
    
    _, status_code = _register_with_single_request(
        registrable_name='uploaders', 
        registrable_func=register_uploader, 
        registrable_list=uploaders
    )
    if status_code != 200: registering_status = False
    

    # # TODO update registry service
    # _, status_code = _register_with_single_request(
    #     registrable_name='report components', 
    #     registrable_func=register_component, 
    #     registrable_list=report_components
    # )
    # if status_code != 200: registering_status = False
        

    
    return registering_status

