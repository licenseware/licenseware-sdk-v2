import requests

from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.logger import log


@authenticated_machine
def register_uploader(**kwargs):
    """
    Send a post request to registry service to make uploader available in front-end
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
                "uploader_id": kwargs["uploader_id"],
                "name": kwargs["name"],
                "description": kwargs["description"],
                "accepted_file_types": kwargs["accepted_file_types"],
                "flags": kwargs["flags"] if len(kwargs["flags"]) > 0 else None,
                "status": kwargs["status"],
                "icon": kwargs["icon"],
                "upload_url": kwargs["upload_url"],
                "upload_validation_url": kwargs["upload_validation_url"],
                "quota_validation_url": kwargs["quota_validation_url"],
                "status_check_url": kwargs["status_check_url"],
                "validation_parameters": kwargs["validation_parameters"],
                "encryption_parameters": kwargs["encryption_parameters"],
            }
        ]
    }

    log.info(payload)
    # validate_register_uploader_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    post_kwargs = dict(url=envs.REGISTER_UPLOADER_URL, json=payload, headers=headers)

    registration = requests.post(**post_kwargs)

    if registration.status_code == 200:
        return {
            "status": "success",
            "message": f"Uploader '{kwargs['uploader_id']}' register successfully",
            "content": payload,
        }, 200

    nokmsg = f"Could not register uploader '{kwargs['uploader_id']}'"
    log.error(nokmsg)
    return {"status": "fail", "message": nokmsg, "content": payload}, 400
