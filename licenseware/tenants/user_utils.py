from typing import List, Union

import requests
from flask import Request

from licenseware.common.constants import envs
from licenseware.utils.logger import log


def user_is_tenant_owner(flask_request: Request):
    """Check from the request given if the current user is the tenant owner"""

    tenant_id = flask_request.headers.get("TenantId")
    auth_token = flask_request.headers.get("Authorization")

    response = requests.get(
        url=envs.AUTH_SERVICE_URL + "/verify-tenant-owner",
        headers={"TenantId": tenant_id, "Authorization": auth_token},
    )

    if response.status_code == 200:
        return True

    return False


def get_user_profile(request_or_auth_headers: Union[Request, dict], field: str = None):
    """

    Get user profile data from auth from the request given

    Usage 1 provide authorization header:
    ```py
        user_email = get_user_profile(
            request_or_auth_headers={
                "TenantId": "the tenant id",
                "Authorization": "the authorization token"
            },
            field = 'email'
        )
    ```

    Usage 2 provide flask request object:
    ```py
        user_email = get_user_profile(
            request_or_auth_headers=request,
            field = 'email'
        )
    ```

    """

    if hasattr(request_or_auth_headers, "headers"):
        tenant_id = request_or_auth_headers.headers.get("TenantId")
        auth_token = request_or_auth_headers.headers.get("Authorization")
    else:
        tenant_id = request_or_auth_headers["TenantId"]
        auth_token = request_or_auth_headers["Authorization"]

    response = requests.get(
        url=envs.AUTH_SERVICE_URL + "/profile",
        headers={"TenantId": tenant_id, "Authorization": auth_token},
    )

    if response.status_code != 200:
        log.error(response.content)
        raise Exception(f"Could not get user profile")

    if field:
        return response.json()[field]

    return response.json()


def get_user_tables(flask_request: Request):

    tenant_id = flask_request.headers.get("TenantId")
    auth_token = flask_request.headers.get("Authorization")

    response = requests.get(
        envs.AUTH_USER_TABLES_URL,
        headers={"TenantId": tenant_id, "Authorization": auth_token},
    )

    if response.status_code == 200:
        return response.json()

    log.info("User's tables not found")


def current_user_has_access_level(flask_request: Request, access_levels: List[str]):

    tables = get_user_tables(flask_request)
    current_tenant = flask_request.headers.get("TenantId")

    # See if current user is tenant owner
    user_tenant = [
        t
        for t in tables["tenants"]
        if t["user_id"] == tables["user"]["id"] and t["id"] == current_tenant
    ]

    if len(user_tenant) == 1:
        return True

    # See if current user is invited as an admin
    user_admin = [
        st
        for st in tables["shared_tenants"]
        if st["invited_email"] == tables["user"]["email"]
        and st["tenant_id"] == current_tenant
        and st["access_level"] in access_levels
    ]

    if len(user_admin) == 1:
        return True

    return False
