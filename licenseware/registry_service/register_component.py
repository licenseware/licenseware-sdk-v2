import requests

from licenseware.common.constants import envs
from licenseware.decorators.auth_decorators import authenticated_machine
from licenseware.utils.logger import log


@authenticated_machine
def register_component(**kwargs):
    """
    Send a post request to registry service to make component available in front-end
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
                "component_id": kwargs["component_id"],
                "url": kwargs["url"],
                "public_url": kwargs["public_url"],
                "snapshot_url": kwargs["snapshot_url"],
                "order": kwargs["order"],
                "style_attributes": kwargs["style_attributes"],
                "attributes": kwargs["attributes"],
                "title": kwargs["title"],
                "component_type": kwargs["component_type"],
                "filters": kwargs["filters"],
            }
        ]
    }

    log.info(payload)
    # validate_register_report_component_payload(payload)

    headers = {"Authorization": envs.get_auth_token()}
    post_kwargs = dict(
        url=envs.REGISTER_REPORT_COMPONENT_URL, json=payload, headers=headers
    )

    registration = requests.post(**post_kwargs)

    if registration.status_code != 200:
        nokmsg = f"Could not register report {kwargs['component_id']}"
        log.error(nokmsg)
        return {"status": "fail", "message": nokmsg, "content": payload}, 500

    return {
        "status": "success",
        "message": f"Report {kwargs['component_id']} registered successfully",
        "content": payload,
    }, 200
