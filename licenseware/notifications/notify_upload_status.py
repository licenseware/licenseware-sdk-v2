from licenseware.common.constants import envs
from licenseware.notifications.uploader_status import save_uploader_status
from licenseware.registry_service import register_upload_status
from licenseware.utils.logger import log


def notify_upload_status(event: dict, status: str):
    """
    Notify registry about uploader processing status
    """

    upload_status = {
        "tenant_id": event["tenant_id"],
        "uploader_id": event["uploader_id"],
        "status": status,
        "app_id": envs.APP_ID,
    }

    log.info(
        f"APP PROCESSING EVENT: {envs.APP_ID} in status: {upload_status}\n for uploader {event['uploader_id']} for tenant {event['tenant_id']}"
    )

    response, status_code = register_upload_status(**upload_status)
    save_uploader_status(**upload_status)

    if status_code != 200:
        return False
    return True
