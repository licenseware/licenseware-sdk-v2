import datetime
import sys
from dataclasses import dataclass
from typing import Tuple

import dateutil.parser as dateparser
from marshmallow import Schema

from licenseware import mongodata
from licenseware.common.constants import envs, states
from licenseware.common.serializers import QuotaSchema
from licenseware.decorators.failsafe_decorator import failsafe
from licenseware.tenants.info import get_tenants_list, get_user_profile


@dataclass
class quota_plan:
    UNLIMITED: str = "UNLIMITED"
    FREE: str = "FREE"


def get_quota_reset_date(current_date: datetime.datetime = datetime.datetime.utcnow()):
    quota_reset_date = current_date + datetime.timedelta(days=30)
    return quota_reset_date.isoformat()


class Quota:
    def __init__(
        self,
        tenant_id: str,
        auth_token: str,
        uploader_id: str,
        units: int,
        schema: Schema = None,
        collection: str = None,
    ):

        self.units = units
        self.tenant_id = (
            tenant_id if not envs.DESKTOP_ENVIRONMENT else envs.DESKTOP_TENANT_ID
        )
        self.auth_token = auth_token
        self.uploader_id = uploader_id
        self.schema = schema or QuotaSchema
        self.collection = collection or envs.MONGO_COLLECTION_UTILIZATION_NAME

        if envs.DESKTOP_ENVIRONMENT:
            self.tenants = [envs.DESKTOP_TENANT_ID]
            self.plan_type = quota_plan.UNLIMITED
        else:
            self.tenants = get_tenants_list(self.tenant_id, self.auth_token)
            self.user_profile = get_user_profile(self.tenant_id, self.auth_token)
            self.plan_type = self.user_profile["plan_type"].upper()

        # This is used to calculate quota
        self.user_query = {
            "tenant_id": {"$in": self.tenants},
            "uploader_id": self.uploader_id,
        }

        # This is used to update quota
        self.tenant_query = {
            "tenant_id": self.tenant_id,
            "uploader_id": self.uploader_id,
        }

        # Making sure quota is initialized
        response, status_code = self.init_quota()
        if status_code != 200:
            # will be cached in the api make sure to add @failsafe(failcode=500) decorator
            raise Exception(response["message"])

    def get_monthly_quota(self):
        if self.plan_type == quota_plan.UNLIMITED:
            return sys.maxsize
        return self.units

    def init_quota(self) -> Tuple[dict, int]:

        results = mongodata.fetch(match=self.tenant_query, collection=self.collection)

        if results:
            return {"status": states.SUCCESS, "message": "Quota initialized"}, 200

        utilization_data = {
            "tenant_id": self.tenant_id,
            "uploader_id": self.uploader_id,
            "monthly_quota": self.get_monthly_quota(),
            "monthly_quota_consumed": 0,
            "quota_reset_date": get_quota_reset_date(),
        }

        inserted_ids = mongodata.insert(
            schema=self.schema, data=utilization_data, collection=self.collection
        )

        if isinstance(inserted_ids, list) and len(inserted_ids) == 1:
            return {"status": states.SUCCESS, "message": "Quota initialized"}, 200

        return {"status": states.FAILED, "message": "Quota failed to initialize"}, 500

    def update_quota(self, units: int) -> Tuple[dict, int]:

        current_utilization = mongodata.fetch(
            match=self.tenant_query, collection=self.collection
        )

        new_utilization = current_utilization[0]
        new_utilization["monthly_quota_consumed"] += units
        _id = new_utilization.pop("_id")

        updated_docs = mongodata.update(
            schema=self.schema,
            match={"_id": _id},
            new_data=new_utilization,
            collection=self.collection,
            append=False,
        )

        if updated_docs != 1:
            return {"status": states.FAILED, "message": "Quota update failed"}, 500

        return {"status": states.SUCCESS, "message": "Quota updated"}, 200

    @failsafe
    def reset_quota(self) -> list:
        quota_data = mongodata.fetch(self.user_query, self.collection)
        quota_reset_date = min(
            [dateparser.parse(quota["quota_reset_date"]) for quota in quota_data]
        )
        current_date = datetime.datetime.utcnow()
        if quota_reset_date <= current_date:
            for quota in quota_data:
                quota["monthly_quota_consumed"] = 0
                quota["quota_reset_date"] = get_quota_reset_date(
                    current_date=quota_reset_date
                )
                quota.pop("_id")
                mongodata.update(
                    schema=self.schema,
                    match=self.user_query,
                    new_data=quota,
                    collection=self.collection,
                    append=False,
                )
        return mongodata.fetch(self.user_query, self.collection)

    def check_quota(self, units: int = 0) -> Tuple[dict, int]:

        if self.plan_type == quota_plan.UNLIMITED:
            return {
                "status": states.SUCCESS,
                "message": "Utilization within monthly quota",
            }, 200

        quota_data = self.reset_quota()

        total_quota_consumed = sum(
            [quota["monthly_quota_consumed"] for quota in quota_data]
        )
        max_allowed_quota = max([quota["monthly_quota"] for quota in quota_data])
        quota_reset_date = min(
            [dateparser.parse(quota["quota_reset_date"]) for quota in quota_data]
        )

        if total_quota_consumed + units <= max_allowed_quota:
            return {
                "status": states.SUCCESS,
                "message": "Utilization within monthly quota",
                "monthly_quota": max_allowed_quota,
                "monthly_quota_consumed": total_quota_consumed,
                "quota_reset_date": quota_reset_date.isoformat(),
            }, 200
        else:
            return {
                "status": states.FAILED,
                "message": "Monthly quota exceeded",
                "monthly_quota": max_allowed_quota,
                "monthly_quota_consumed": total_quota_consumed,
                "quota_reset_date": quota_reset_date.isoformat(),
            }, 402
