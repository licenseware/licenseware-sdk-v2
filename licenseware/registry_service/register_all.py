import requests

from licenseware.common.constants import envs
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.logger import log


class RegistrationFailed(Exception):
    ...


def registration_failed(retries_so_far: int, exception):
    return isinstance(exception, RegistrationFailed)


@broker.actor(retry_when=registration_failed, queue_name=envs.QUEUE_NAME)
def register_all(payload: dict):

    if envs.DESKTOP_ENVIRONMENT:
        return

    log.info("Sending payload to registry-service")

    registration = requests.post(
        url=envs.REGISTER_ALL_URL,
        json=payload,
        headers={
            "Authorization": envs.get_auth_token(),
            "Content-type": "application/json",
            "Accept": "application/json",
        },
    )

    if registration.status_code != 200:
        log.warning(registration.content)
        raise RegistrationFailed("Registration failed")

    log.success("Registration successful!")
