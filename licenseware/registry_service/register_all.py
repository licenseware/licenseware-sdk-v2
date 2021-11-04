# from .register_all_single_requests import register_all_single_requests
import requests
from licenseware.common.constants import envs
from licenseware.utils.logger import log
from licenseware.utils.dramatiq_redis_broker import broker


class RegistrationFailed(Exception): ...


def registration_failed(retries_so_far:int, exception):
    return isinstance(exception, RegistrationFailed)


@broker.actor(
    retry_when=registration_failed,
    queue_name=envs.QUEUE_NAME
)
def register_all(payload:dict):
    
    # Delete this comented block
    # registration_done = register_all_single_requests(
    #     event['app'], 
    #     event['reports'], 
    #     event['report_components'], 
    #     event['uploaders']
    # )
    
    
    log.info(payload)    

    registration = requests.post(
        url=envs.REGISTER_ALL_URL, 
        json=payload, 
        headers={"Authorization": envs.get_auth_token()}
    )
    
    if registration.status_code != 200:
        raise RegistrationFailed("Registration failed")

