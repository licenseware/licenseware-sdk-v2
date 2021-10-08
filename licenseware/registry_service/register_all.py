from pymongo.errors import ExecutionTimeout
from .register_all_multiple_requests import register_all_multiple_requests
from .register_all_single_requests import register_all_single_requests

from licenseware.common.constants import envs
from licenseware.utils.dramatiq_redis_broker import broker



@broker.actor(
    max_retries=100, 
    min_backoff=1000, 
    queue_name=envs.APP_ID.replace('-service', '')
)
def register_all(event:dict):

    registration_done = False
    
    if event['single_request']: 
        registration_done = register_all_single_requests(
            event['app'], 
            event['reports'], 
            event['report_components'], 
            event['uploaders']
        )
    else:
        registration_done = register_all_multiple_requests(
                event['app'], 
                event['reports'], 
                event['report_components'], 
                event['uploaders']
            )
        
    if not registration_done:
        raise Exception("Registration failed")
    
    