from licenseware.registry_service import register_upload_status
from licenseware.utils.logger import log
from licenseware.common.constants import envs


def notify_upload_status(event: dict, status: str):
    """
        Notify registry about uploader processing status
    """

    status = {
        'tenant_id': event['tenant_id'],
        'uploader_id': event['uploader_id'],
        'status': status,
        'app_id': envs.APP_ID
    }

    log.info(
        f"APP PROCESSING EVENT: {envs.APP_ID} in status {status} for uploader {event['uploader_id']} for tenant event['tenant_id']")

    response, status_code = register_upload_status(**status)

    if status_code != 200:
        return False
    return True
