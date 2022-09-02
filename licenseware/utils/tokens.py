import datetime

import dateutil.parser as dateparser
import jwt

from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.common.serializers import PublicTokenSchema


def valid_public_token(public_token: str):

    results = mongodata.fetch(
        match={"token": public_token}, collection=envs.MONGO_COLLECTION_TOKEN_NAME
    )

    if not results:
        return False

    now = datetime.datetime.utcnow()
    exp = dateparser.parse(results[0]["expiration_date"])

    if now > exp:
        mongodata.delete(
            match={"token": public_token}, collection=envs.MONGO_COLLECTION_TOKEN_NAME
        )
        return False

    return True


def get_public_token(
    tenant_id: str, expire: int, report_id: str, ui_public_url: str, api_public_url: str
):

    token = jwt.encode(
        {
            "tenant_id": tenant_id,
            "expire": expire,
            "app_id": envs.APP_ID,
            "report_id": report_id,
            "ui_public_url": ui_public_url,
            "public_url": api_public_url,
        },
        envs.SECRET,
        algorithm="HS256",
    )

    data = dict(
        tenant_id=tenant_id,
        report_id=report_id,
        app_id=envs.APP_ID,
        token=token,
        expiration_date=(
            datetime.datetime.utcnow() + datetime.timedelta(minutes=expire)
        ).isoformat(),
    )

    if valid_public_token(token):
        return token

    mongodata.insert(
        schema=PublicTokenSchema, data=data, collection=envs.MONGO_COLLECTION_TOKEN_NAME
    )

    return token


def get_public_token_data(token: str):
    data = jwt.decode(token, envs.SECRET, algorithm="HS256")
    return data


def delete_public_token(tenant_id: str, report_id: str):

    mongodata.delete(
        match={"tenant_id": tenant_id, "report_id": report_id, "app_id": envs.APP_ID},
        collection=envs.MONGO_COLLECTION_TOKEN_NAME,
    )

    return "Public token deleted"
