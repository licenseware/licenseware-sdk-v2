"""

This endpoint is called for reprocessing the data by tenant.

"""

import os
import uuid

import requests
from flask import request
from flask_restx import Api, Resource
from marshmallow import Schema, fields

from licenseware.common.constants import envs
from licenseware.common.marshmallow_restx_converter import marshmallow_to_restx_model
from licenseware.decorators import failsafe
from licenseware.mongodata import aggregate
from licenseware.report_components import ExternalDataService
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.logger import log


class ReprocessSchema(Schema):
    tenants = fields.List(fields.String, allow_none=True, required=False)
    password = fields.String(required=True)


def get_uploads(tenant_id):

    pipeline = [
        # TODO add valdiation
        {"$sort": {"updated_at": 1}},
        {
            "$group": {
                "_id": ["$tenant_id", "$uploader_id"],
                "date": {"$last": "$updated_at"},
                "uploader_id": {"$last": "$uploader_id"},
                "files_uploaded": {"$last": "$files_uploaded"},
                "tenant_id": {"$last": "$tenant_id"},
            }
        },
    ]

    if tenant_id is not None:
        pipeline = [{"$match": {"tenant_id": tenant_id}}] + pipeline

    uploads = aggregate(pipeline, collection=envs.MONGO_COLLECTION_HISTORY_NAME)
    return uploads


def get_files(files_uploaded):
    file_list = []
    for fpath in files_uploaded:
        fname = os.path.basename(fpath)
        file_list.append(("files[]", (fname, open(fpath, "rb"))))
    return file_list


@broker.actor(max_retries=0, queue_name=envs.QUEUE_NAME)
def send_files(dataset):
    """
    External Data Service handles the machine token.

    Tenant + machine token doesn't work.
    """
    auth_headers = {
        "Tenantid": dataset["tenant_id"],
        "Authorization": envs.get_auth_token(),
    }

    upload_url = ExternalDataService.get_upload_url(
        _request=auth_headers, app_id=envs.APP_ID, uploader_id=dataset["uploader_id"]
    )
    if "backend.localhost" in upload_url:
        upload_url = upload_url.replace("backend.localhost", "kong")

    res = requests.post(
        upload_url, files=get_files(dataset["files_uploaded"]), headers=auth_headers
    )

    if res.status_code != 200:
        log.warning(res.content)
        log.error(
            f"""
            Failed to send files for uploader_id: {dataset["uploader_id"]} for Tenant: {dataset["tenant_id"]} 
        """
        )


@broker.actor(max_retries=0, queue_name=envs.QUEUE_NAME)
def reprocess_files(tenants):

    if not tenants:
        for dataset in get_uploads(None):
            send_files.send(dataset)

    for tenant_id in tenants:
        for dataset in get_uploads(tenant_id):
            send_files.send(dataset)


def add_reprocess_data_route(api: Api, appvars: dict):

    model = marshmallow_to_restx_model(api, ReprocessSchema)

    @api.route(appvars["reprocess_data_path"])
    class ReprocessTenantData(Resource):
        @failsafe(fail_code=500)
        @api.doc(
            description="Reprocess latest file for tenant_id",
            responses={
                200: "Reprocessing started",
                403: "Password doesn't match!",
                500: "Something went wrong while handling the request",
            },
        )
        @api.expect(model, validate=True)
        def post(self):

            if "6202b399-b79b-59ff-9925-5ab1534d324d" != str(
                uuid.uuid5(uuid.NAMESPACE_DNS, str(request.json["password"]))
            ):
                log.warning("Password on `reprocess_files` didn't match")
                return "Password doesn't match!", 403

            reprocess_for_tenants = request.json.get("tenants")

            reprocess_files.send(tenants=reprocess_for_tenants)

            return "Reprocessing started", 200

    return api
