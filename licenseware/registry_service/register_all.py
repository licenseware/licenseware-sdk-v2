from .register_all_single_requests import register_all_single_requests

from licenseware.common.constants import envs
from licenseware.utils.dramatiq_redis_broker import broker


class RegistrationFailed(Exception): ...


def registration_failed(retries_so_far:int, exception):
    return isinstance(exception, RegistrationFailed)


@broker.actor(
    retry_when=registration_failed,
    queue_name=envs.APP_ID.replace('-service', '')
)
def register_all(event:dict):
    
    registration_done = register_all_single_requests(
        event['app'], 
        event['reports'], 
        event['report_components'], 
        event['uploaders']
    )
    
    if not registration_done:
        raise RegistrationFailed("Registration failed")
    
    