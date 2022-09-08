from licenseware import mongodata as m
from licenseware.common.constants import envs, states
from licenseware.tenants.close_timeout_files import close_timed_out_files
from licenseware.utils.logger import log

#! OUTDATED


def get_processing_status(tenant_id: str):
    """
    Get processing status for a tenant_id from all uploaders
    """

    close_timed_out_files()

    query = {
        "tenant_id": tenant_id,
        "$or": [{"files.status": states.RUNNING}, {"status": states.RUNNING}],
    }

    results = m.document_count(
        match=query, collection=envs.MONGO_COLLECTION_ANALYSIS_NAME
    )

    log.info(results)

    if results > 0:
        return {"status": states.RUNNING}, 200
    return {"status": states.IDLE}, 200


def get_uploader_status(tenant_id: str, uploader_id: str):
    """
    Get processing status for a tenant_id and the specified uploader
    """

    close_timed_out_files()

    query = {
        "tenant_id": tenant_id,
        "uploader_id": uploader_id,
        "$or": [{"files.status": states.RUNNING}, {"status": states.RUNNING}],
    }

    results = m.document_count(
        match=query, collection=envs.MONGO_COLLECTION_ANALYSIS_NAME
    )

    log.info(results)

    if results > 0:
        return {"status": states.RUNNING}, 200
    return {"status": states.IDLE}, 200
