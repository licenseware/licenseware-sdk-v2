import sys
import unittest

from licenseware.quota import Quota
from licenseware.utils.logger import log

from . import tenant_id

# python3 -m unittest tests/test_quota.py


class TestQuota(unittest.TestCase):
    def test_quota(self):

        # uploader_id = envs.PERSONAL_SUFFIX + 'rv_tools'
        uploader_id = "rv_tools"
        auth_token = "asdasdededed"

        q = Quota(tenant_id, auth_token, uploader_id, units=sys.maxsize)

        response, status_code = q.init_quota()
        self.assertEqual(status_code, 200)

        response, status_code = q.update_quota(units=1)
        self.assertEqual(status_code, 200)

        response, status_code = q.check_quota(units=1)
        log.debug(response)
        self.assertEqual(status_code, 200)
