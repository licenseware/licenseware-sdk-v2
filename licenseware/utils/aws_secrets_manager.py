# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.create_secret
import json
import os
from typing import Union

import boto3


class SecretsManager:
    """
    Usage:

    ```py

    from services import SecretsManager

    secret_id = "secret_data"
    data = {
        "secret_data": 123123
    }

    SecretsManager.create_secret(secret_id, data)
    data_from_secret = SecretsManager.get_secret(secret_id)
    SecretsManager.delete_secret(secret_id)
    SecretsManager.update_secret(secret_id, data)

    ```
    """

    @classmethod
    def get_client(cls):
        """
        Get boto3 client secretsmanager aws service
        """

        region = os.getenv("AWS_REGION", "eu-central-1")
        session = boto3.session.Session()

        client = session.client(service_name="secretsmanager", region_name=region)

        return client

    @classmethod
    def create_secret(cls, secret_id: str, data: Union[str, dict, list]):
        """
        Save in aws secrets manager the `data` provided at `secret_id` location
        You can later use `secret_id` location to retreive the secrets.
        """

        client = cls.get_client()

        if type(data) in [dict, list]:
            data = json.dumps(data)

        response = client.create_secret(
            Name=secret_id, SecretString=data, ForceOverwriteReplicaSecret=True
        )

        return response["secret_id"]

    @classmethod
    def get_secret(cls, secret_id: str):
        """
        Use `secret_id` provided on `create_secret` to retreive the secrets.
        """

        client = cls.get_client()
        response = client.get_secret_value(SecretId=secret_id)

        try:
            return json.loads(response["SecretString"])
        except:
            return response["SecretString"]

    @classmethod
    def delete_secret(cls, secret_id: str):
        """
        Delete secrets at `secret_id` location
        """

        client = cls.get_client()

        return client.delete_secret(SecretId=secret_id, ForceDeleteWithoutRecovery=True)

    @classmethod
    def update_secret(cls, secret_id: str, data: Union[str, dict, list]):
        """
        Update secrets at `secret_id` location
        """

        cls.delete_secret(secret_id)
        cls.create_secret(secret_id, data)

        return secret_id
