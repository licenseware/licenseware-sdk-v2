import datetime

import dateutil.parser as dateparser

from licenseware import mongodata
from licenseware.common.constants import envs, states
from licenseware.common.serializers import WildSchema


def save_uploader_status(tenant_id: str, uploader_id: str, status: str, **overflow):

    # Not great, a history based implementations needs to be made or something else
    # Somehow we should mark the last function in the processing pipeline as the last one
    # @history.log(end=True)
    # def the_processing_func_that_runs_at_the_end():
    #     pass
    # Within a loop that would be pretty hard to figure out
    # Also, pretty hard to keep track of threads and multiprocessing
    # This will work in most cases, but some issues may appear when multiple uploads are made consecutively

    if envs.DESKTOP_ENVIRONMENT and tenant_id is None:
        tenant_id = envs.DESKTOP_TENANT_ID

    data = {
        "tenant_id": tenant_id,
        "uploader_id": uploader_id,
        "app_id": envs.APP_ID,
        "status": status,
        "last_update": datetime.datetime.utcnow().isoformat(),
    }

    mongodata.update(
        schema=WildSchema,
        match={
            "tenant_id": tenant_id,
            "uploader_id": uploader_id,
            "app_id": envs.APP_ID,
        },
        new_data=data,
        collection=envs.MONGO_COLLECTION_UPLOADERS_STATUS_NAME,
    )


def get_uploader_status(tenant_id: str, uploader_id: str):

    if envs.DESKTOP_ENVIRONMENT and tenant_id is None:
        tenant_id = envs.DESKTOP_TENANT_ID

    results = mongodata.fetch(
        match={
            "tenant_id": tenant_id,
            "uploader_id": uploader_id,
            "app_id": envs.APP_ID,
        },
        collection=envs.MONGO_COLLECTION_UPLOADERS_STATUS_NAME,
    )

    if not results:
        return {"status": states.IDLE}

    data = results[0]

    current_date = datetime.datetime.utcnow()
    last_update = dateparser.parse(data["last_update"])
    delta_minutes = (current_date - last_update).total_seconds() / 60

    if delta_minutes > 180:  # 3h
        save_uploader_status(tenant_id, uploader_id, status=states.IDLE)
        return {"status": states.IDLE}

    return {"status": data["status"]}, 200
