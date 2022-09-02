import requests

from licenseware.common.constants import envs
from licenseware.utils.logger import log


def get_tenants_list(tenant_id: str, auth_token: str):

    response = requests.get(
        url=envs.AUTH_TENANTS_URL + "/quota-tenants",
        headers={"TenantId": tenant_id, "Authorization": auth_token},
    )

    if response.status_code == 200:
        return response.json()
    else:
        log.info(response.content)
        return []


def get_user_profile(tenant_id: str, auth_token: str):

    response = requests.get(
        url=envs.AUTH_USER_PROFILE_URL,
        headers={"TenantId": tenant_id, "Authorization": auth_token},
    )

    if response.status_code == 200:
        return response.json()
    else:
        log.warning(response.content)
        return None
