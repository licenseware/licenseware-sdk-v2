import os
import time
from datetime import datetime

import requests

from licenseware.common.constants import envs
from licenseware.utils.logger import log


class Authenticator:
    """

    Licenseware authentification

        `from licenseware.auth import Authenticator`

        `response, status_code = Authenticator.connect()`

    Response is a tuple: json, status code

    Since apps can't work without being authentificated you can set `max_retries` to 'infinite'.
    Doing that if authentification failed for some reason it will try to authentificate again.

        `response, status_code = Authenticator.connect(max_retries='infinite', wait_seconds=2)`



    Requirements:

    Set login values in environment variables:
    - LWARE_IDENTITY_USER (the email/machine_name)
    - LWARE_IDENTITY_PASSWORD (the password)
    - AUTH_SERVICE_URL (url to authentification service)


    """

    def __init__(self):

        self.machine_name = envs.LWARE_USER
        self.password = envs.LWARE_PASSWORD
        self.auth_url = envs.AUTH_MACHINES_URL
        self.auth_login_url = f"{self.auth_url}/login"
        self.auth_create_url = f"{self.auth_url}/create"

    @classmethod
    def connect(cls, max_retries: int = 0, wait_seconds: int = 1):
        """
        Connects to licenseware and saves in environment variables auth tokens.

        param: max_retries  - 'infinite' or a number,
        param: wait_seconds - wait time in seconds if authentification fails

        """
        if os.getenv("AUTH_SERVICE_URL") is None:
            log.error(
                "Environment variable `AUTH_SERVICE_URL` not available. Skipping machine authentification."
            )
            return "Environment variable `AUTH_SERVICE_URL` not available", 500

        status_code = 500

        if max_retries == "infinite":
            while status_code != 200:
                response, status_code = cls()._retry_login()
                time.sleep(wait_seconds)
        else:
            for _ in range(max_retries + 1):
                response, status_code = cls()._retry_login()
                if status_code == 200:
                    break
                time.sleep(wait_seconds)

        if status_code == 200:
            os.environ["AUTH_TOKEN"] = response.get(
                "Authorization", "Authorization not found"
            )
            os.environ["AUTH_TOKEN_DATETIME"] = datetime.utcnow().isoformat()
            os.environ["APP_AUTHENTICATED"] = "true"
        else:
            os.environ["APP_AUTHENTICATED"] = "false"
            log.error(response)

        return response, status_code

    def _retry_login(self):
        response, status_code = {"status": "failed"}, 500
        try:
            response, status_code = self._login()
        except Exception as err:
            log.error(f"{str(err)}\n\nAuthentification failed... retrying... ")
            pass  # ConnectionError
        return response, status_code

    def _login(self):

        payload = {"machine_name": self.machine_name, "password": self.password}

        response = requests.post(self.auth_login_url, json=payload)

        if response.status_code == 200:
            return response.json(), 200

        log.error(f"Could not login with {self.machine_name}")
        exit(1)
