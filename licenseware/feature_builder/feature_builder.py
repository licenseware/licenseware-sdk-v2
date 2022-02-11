from typing import List
from flask import Request
from licenseware.quota import Quota
from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.common.serializers import FeaturesSchema
from licenseware.tenants.user_utils import current_user_has_access_level


class FeatureBuilder:

    def __init__(self,
        name: str,
        description: str = None,
        access_levels: List[str] = None,
        free_quota: int = 1,
        activated: bool = False,
        feature_id: str = None,
        feature_path: str = None
    ):
        self.name = name
        self.description = description
        self.access_levels = access_levels
        self.free_quota = free_quota
        self.activated = activated
        self.feature_id = feature_id
        self.feature_path = feature_path

        self.get_details()

        

    def get_details(self):

        # ! There can't be 2 features with the same `name`
        # `decorators` will be applied on the route created
        # `access_levels` will be verified with auth 
        #  Ex: 
        #  access_levels = ['admin'] will check 
        #  `shared_tenant` table `access_level` column for `admin` value
        #  or if user is the tenant owner

        if self.feature_id is None:
            self.feature_id = self.name.lower().replace(" ", "_")

        if self.feature_path is None:
            self.feature_path = '/' + self.feature_id.replace("_", "-")

        return {
            'name': self.name,
            'description': self.description,
            'access_levels': self.access_levels,
            'free_quota': self.free_quota,
            'activated': self.activated,
            'feature_id': self.feature_id,
            'feature_path': self.feature_path
        }

    def update_quota(self, flask_request: Request, units: int = 1):

        q = Quota(
            tenant_id=flask_request.headers.get("TenantId"),
            auth_token=flask_request.headers.get("Authorization"),
            units=self.free_quota,
            uploader_id=self.feature_id
        )

        res, status_code = q.check_quota(units)
        if status_code == 200:
            return q.update_quota(units)

        return res, status_code

    def get_status(self, flask_request: Request):

        tenant_id = flask_request.headers.get("TenantId")

        results = mongodata.fetch(
            match={'tenant_id': tenant_id, "name": self.name},
            collection=envs.MONGO_COLLECTION_FEATURES_NAME
        )

        return results, 200

    def set_status(self, tenant_id: str, status: bool):

        self.activated = status
        feature_details = self.get_details()

        updated = mongodata.update(
            schema=FeaturesSchema,
            match={'tenant_id': tenant_id, 'name': self.name},
            new_data=feature_details,
            collection=envs.MONGO_COLLECTION_FEATURES_NAME
        )

        return updated

    def update_status(self, flask_request: Request):

        status = flask_request.json['activated']
        tenant_id = flask_request.headers.get("TenantId")

        resp = f"Feature {'activated' if status else 'deactivated'}", 200

        if len(self.access_levels) == 0:
            self.set_status(tenant_id, status)
            return resp

        if current_user_has_access_level(flask_request, self.access_levels):
            self.set_status(tenant_id, status)
            return resp

        return "Not enough rights to activate/deactivate feature", 401
