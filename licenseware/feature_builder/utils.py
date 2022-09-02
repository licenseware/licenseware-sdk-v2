from flask import Request

from licenseware import mongodata
from licenseware.common.constants import envs


def get_all_features(flask_request: Request):

    tenant_id = flask_request.headers.get("TenantId")

    results = mongodata.fetch(
        match=({"tenant_id": tenant_id}, {"_id": 0, "activated": 0}),
        collection=envs.MONGO_COLLECTION_FEATURES_NAME,
    )

    return results
