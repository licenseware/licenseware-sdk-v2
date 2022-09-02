from typing import List

from flask import request
from flask_restx import Namespace, Resource, fields

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.uploader_builder import UploaderBuilder


def create_uploader_resource(uploader: UploaderBuilder):
    class UploaderQuota(Resource):
        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            return uploader.check_tenant_quota(
                tenant_id=request.headers.get("Tenantid"),
                auth_token=request.headers.get("Authorization"),
            )

    return UploaderQuota


def get_quota_namespace(ns: Namespace, uploaders: List[UploaderBuilder]):

    quota_model = ns.model(
        "quota_model_response",
        {
            "status": fields.String(
                required=True,
                description="Failed or Success depending if quota is exceeded",
            ),
            "message": fields.String(
                required=True,
                description="`Utilization within monthly quota` or `Monthly quota exceeded`",
            ),
            "monthly_quota": fields.Integer(
                required=True,
                description="How much quota is allowed for free per month",
            ),
            "monthly_quota_consumed": fields.Integer(
                required=True, description="How much quota is currently consumed"
            ),
            "quota_reset_date": fields.String(
                required=True,
                description="Iso date when the monthly quota will be reset",
            ),
        },
    )

    for uploader in uploaders:

        if uploader.quota_units is None:
            continue

        UR = create_uploader_resource(uploader)

        @ns.doc(
            description="Check if tenant has quota within limits",
            responses={
                400: "Tenantid not provided",
                402: "Monthly quota exceeded",
                403: "Missing `Tenant` or `Authorization` information",
                500: "Something went wrong while handling the request",
            },
        )
        @ns.response(
            code=200, description="Utilization within monthly quota", model=quota_model
        )
        class TempUploaderResource(UR):
            ...

        UploaderResource = type(
            uploader.uploader_id.replace("_", "").capitalize() + "quota",
            (TempUploaderResource,),
            {},
        )

        ns.add_resource(UploaderResource, uploader.quota_validation_path)

    return ns
