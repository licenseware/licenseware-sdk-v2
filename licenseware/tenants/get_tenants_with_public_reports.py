from datetime import datetime

from licenseware import mongodata
from licenseware.common.constants import envs


def get_tenants_with_public_reports(
    *, report_id: str = None, tenant_id: str = None
) -> list:

    if envs.DESKTOP_ENVIRONMENT:
        return []

    query = {
        "tenant_id": tenant_id or {"$exists": True},
        "report_id": report_id or {"$exists": True},
        "expiration_date": {"$gt": datetime.utcnow().isoformat()},
    }

    projection = {"_id": 0, "expiration_date": 0, "app_id": 0, "token": 0}

    if report_id is None:
        projection.update({"report_id": 0})

    tenants = mongodata.fetch(
        match=(query, projection), collection=envs.MONGO_COLLECTION_TOKEN_NAME
    )

    if report_id is None:
        return [d["tenant_id"] for d in tenants]
    return tenants
