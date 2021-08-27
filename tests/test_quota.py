import unittest
from app.licenseware.utils.logger import log
from app.licenseware.quota import Quota
from . import tenant_id


# python3 -m unittest tests/test_quota.py



class TestQuota(unittest.TestCase):
    
    def test_quota(self):
        
        uploader_id = 'rv_tools'
        units = 1
        
        q = Quota(tenant_id, uploader_id, units)
        
        response, status_code = q.init_quota()
        self.assertEqual(status_code, 200)
        
        response, status_code = q.update_quota(units=1)
        self.assertEqual(status_code, 200)
        
        response, status_code = q.check_quota(units=1)
        self.assertEqual(status_code, 200)
        