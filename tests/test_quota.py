import unittest
from app.licenseware.utils.logger import log
from app.licenseware.quota import Quota
from app.licenseware.common.constants import envs
from . import tenant_id
import sys

# python3 -m unittest tests/test_quota.py



class TestQuota(unittest.TestCase):
    
    def test_quota(self):
        
        # uploader_id = envs.PERSONAL_SUFFIX + 'rv_tools'
        uploader_id = 'rv_tools'
        
        q = Quota(tenant_id, uploader_id, units=sys.maxsize)
        
        response, status_code = q.init_quota()
        self.assertEqual(status_code, 200)
        
        response, status_code = q.update_quota(units=1)
        self.assertEqual(status_code, 200)
        
        response, status_code = q.check_quota(units=1)
        log.debug(response)
        self.assertEqual(status_code, 200)
        