import datetime
import unittest

from marshmallow import fields

from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.common.serializers.quota_schema import QuotaSchema
from licenseware.tenants.active_tenants import (
    get_activated_tenants,
    get_tenants_with_data,
)
from licenseware.utils.logger import log

from . import tenant_id

# python3 -m unittest tests/test_tenants_info.py


class DataSchema(QuotaSchema):
    updated_at = fields.Str(required=False)


class TestTenants(unittest.TestCase):
    def setUp(self):

        self.utilization_collection = envs.MONGO_COLLECTION_UTILIZATION_NAME

        mongodata.insert(
            schema=QuotaSchema,
            collection=self.utilization_collection,
            data=dict(
                user_id=tenant_id,
                tenant_id=tenant_id,
                uploader_id="rv_tools",
                monthly_quota=1,
                monthly_quota_consumed=5,
                quota_reset_date="some date",
            ),
        )

        self.data_collection = envs.MONGO_COLLECTION_DATA_NAME

        mongodata.insert(
            schema=DataSchema,
            collection=self.data_collection,
            data=dict(
                user_id=tenant_id,
                tenant_id=tenant_id,
                uploader_id="rv_tools",
                monthly_quota=1,
                monthly_quota_consumed=5,
                quota_reset_date="some date",
                updated_at=datetime.datetime.utcnow().isoformat(),
            ),
        )

    def tearDown(self):
        mongodata.delete_collection(self.utilization_collection)
        mongodata.delete_collection(self.data_collection)

    def test_activated_tenants(self):

        activated_tenants = get_activated_tenants(tenant_id)
        log.debug(activated_tenants)
        self.assertGreater(len(activated_tenants), 0)

        tenants_with_data = get_tenants_with_data(tenant_id)
        log.debug(tenants_with_data)
        self.assertGreater(len(tenants_with_data), 0)
