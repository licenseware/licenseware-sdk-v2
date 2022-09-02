import requests

from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.logger import log


@authenticated_machine
def register_report(**kwargs):

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
                "report_id": kwargs["report_id"],
                "name": kwargs["name"],
                "description": kwargs["description"],
                "flags": kwargs["flags"],
                "url": kwargs["url"],
                "public_url": kwargs["public_url"],
                "snapshot_url": kwargs["snapshot_url"],
                "preview_image_url": kwargs["preview_image_url"],
                "preview_image_dark_url": kwargs["preview_image_dark_url"],
                "report_components": kwargs["report_components"],
                "connected_apps": kwargs["connected_apps"],
                "filters": kwargs["filters"],
                "public_for_tenants": kwargs["public_for_tenants"],
                "registrable": kwargs["registrable"],
            }
        ]
    }

    log.info(payload)
    # validate_register_report_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    post_kwargs = dict(url=envs.REGISTER_REPORT_URL, json=payload, headers=headers)

    registration = requests.post(**post_kwargs)

    if registration.status_code != 200:
        nokmsg = f"Could not register report {kwargs['name']}"
        log.error(nokmsg)
        return {"status": "fail", "message": nokmsg, "content": payload}, 500

    return {
        "status": "success",
        "message": f"Report {kwargs['name']} registered successfully",
        "content": payload,
    }, 200
