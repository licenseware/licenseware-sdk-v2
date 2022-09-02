import requests

from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.logger import log


@authenticated_machine
def register_upload_status(**kwargs):
    """
    Send uploader processing status to registry service
    """

    if envs.DESKTOP_ENVIRONMENT:
        return {
            "status": "success",
            "message": "Skipped on desktop environment",
            "content": kwargs,
        }, 200

    payload = {
        "data": [
            {
                "app_id": kwargs["app_id"],
                "tenant_id": kwargs["tenant_id"],
                "uploader_id": kwargs["uploader_id"],
                "status": kwargs["status"],
            }
        ]
    }

    log.info(payload)
    # validate_register_uploader_status_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    response = requests.post(
        url=envs.REGISTER_UPLOADER_STATUS_URL, headers=headers, json=payload
    )

    if response.status_code == 200:
        log.info("Notification registry service success!")
        return {"status": "success", "message": payload, "content": payload}, 200

    log.error("Notification registry service failed!")
    return {"status": "fail", "message": payload, "content": payload}, 500
