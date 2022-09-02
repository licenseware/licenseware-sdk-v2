"""

The `AuthHelper` class can be used to obtain authorization headers from auth service + other interactions with auth.

```py
from licenseware.test_helpers.auth import AuthHelper
```

Here we provide an email and call the `get_auth_headers` method
which will return the auth headers (TenantId and Authorization) needed for making a request auth

```py
auth_headers = AuthHelper(main_admin).get_auth_headers()
```

Here we are accepting the invitation on a tenant_id(project)

```py

for email in [admin_email1, user_email1]:
    response = AuthHelper(email).accept_invite_on_tenant(auth_headers['TenantId'])
    assert response

```

We can set a default tenant/project
```py
auth_headers = AuthHelper(email, default_tenant="1234").get_auth_header()
```
This way the `default_tenant` will be used for the request

"""

import requests

from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.logger import log


class AuthHelper:
    def __init__(
        self, email: str, password: str = "secret", default_tenant: str = None
    ):
        self.email = email
        self.password = password
        self.default_tenant = default_tenant
        self.auth_headers = self.get_auth_headers()

    @authenticated_machine
    def get_auth_headers(self):
        """
        Get required auth headers needed to make a request as a user
        """

        login_response = self.login_user(self.email, self.password)

        if login_response["status"] == "success":
            login_response.pop("status")
            login_response.pop("message")
            log.success(login_response)
            if self.default_tenant is not None:
                login_response["TenantId"] = self.default_tenant
            return login_response
        else:
            self.create_user(self.email, self.password)
            return self.get_auth_headers()

    def accept_invite_on_tenant(self, tenant_id: str):

        log.debug(f"Getting invite token for '{self.email}' on tenant '{tenant_id}'")

        invite_token = self.get_invite_token(tenant_id)

        if invite_token is None:
            raise Exception("No invite token found")

        log.debug(f"Logging '{self.email}' with invite token: '{invite_token}'")

        response = requests.post(
            envs.AUTH_SERVICE_URL + "/login",
            json={"email": self.email, "password": self.password},
            params={"invite_token": invite_token},
        )

        log.warning(f"Response from logging with invite token: {response.content}")

        return response.json()

    def get_invite_token(self, tenant_id: str):

        shared_tenants = self.get_auth_tables("shared_tenants")

        for st in shared_tenants:
            if st["invited_email"] == self.email and st["tenant_id"] == tenant_id:
                log.success(f"Found invite token '{st['invite_token']}'")
                return st["invite_token"]

    def get_auth_tables(self, table: str = None):
        """
        Tables: users, tenants, shared_tenants
        """

        response = requests.get(
            envs.AUTH_SERVICE_URL + "/users/tables", headers=self.auth_headers
        )

        log.debug(f"User's tables: {response.json()}")

        if table:
            return response.json()[table]

        return response.json()

    @staticmethod
    def login_user(email: str, password: str):

        response = requests.post(
            envs.AUTH_SERVICE_URL + "/login",
            json={"email": email, "password": password},
        )

        # log.debug(response.content)

        return response.json()

    @staticmethod
    def create_user(
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        company_name: str = None,
        job_title: str = None,
    ):

        payload = {
            "email": email,
            "password": password,
            "first_name": first_name or email.split("@")[0],
            "last_name": last_name or "",
            "company_name": company_name or email.split("@")[1].split(".")[0],
            "job_title": job_title or "",
        }

        response = requests.post(
            envs.AUTH_SERVICE_URL + "/users/register", json=payload
        )

        # log.debug(response)

        return response.json()
