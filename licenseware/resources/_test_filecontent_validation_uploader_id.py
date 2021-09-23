import os, time
import unittest
from . import headers, get_mock_binary_files, tenant_id
from main import app, App

from licenseware.utils.logger import log
from licenseware.common.constants import envs, states
from licenseware.uploader_validator import UploaderValidator

from licenseware import mongodata
from licenseware.tenants.processing_status import get_uploader_status

# python3 -m unittest tests/test_filecontent_validation_{{ uploader_id }}.py



uploader_id = '{{ uploader_id }}'


class Test{{ uploader_id }}Content(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True
        self.app = app.test_client()
        
    
    def test_filecontent_validation(self):
        
        url = None
        for uploader in App.uploaders:
            if uploader.uploader_id == uploader_id:
                url = envs.APP_PATH + envs.UPLOAD_PATH + uploader.upload_path
                break
        
        log.debug(uploader.uploader_id)
        log.debug(url)
        
        self.assertNotEqual(url, None)
        
        mock_binary_files = get_mock_binary_files(f'test_files/{uploader_id}')
        
        response = self.app.post(
            url, 
            headers = headers,
            data = mock_binary_files
        )
        
        log.warning(response.json)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        
        file_paths = UploaderValidator.get_filepaths_from_objects_response(response.json)
    
        [self.assertEqual(os.path.exists(fp), True) for fp in file_paths]
        
        
        # Waiting for data to be written   
        time.sleep(3)  
        uploader_response, _ = get_uploader_status(tenant_id, uploader_id=uploader.uploader_id)
        while uploader_response['status'] == states.RUNNING:
            uploader_response, _ = get_uploader_status(tenant_id, uploader_id=uploader.uploader_id)
            log.debug(uploader_response)
            time.sleep(1)
            
            
    
    def test_mongo_data_saved(self):
        
        # device_name = 'T7CNTC4'
        # databases = ['DBHOST2', 'DBLOPD', 'DBTRILLO', 'DBTRPER']
        
        # files = []
        # [
        #     files.extend([
        #         f'{device_name}_{db}_version.csv', 
        #         f'{device_name}_{db}_options.csv', 
        #         f'{device_name}_{db}_dba_feature.csv'
        #     ]) for db in databases
        # ]
        
        # log.info(files)
    
        # data_saved = mongodata.fetch(
        #     match={
        #         'tenant_id': tenant_id,
        #         'database_name': { '$in': databases },
        #         'device_name': device_name,
        #     }, 
        #     collection=envs.MONGO_COLLECTION_DATA_NAME
        # )
        
        # self.assertGreater(len(data_saved), 0)
        
                
        # stats_saved = mongodata.fetch(
        #     match={
        #         'tenant_id': tenant_id,
        #         'uploader_id': uploader_id,
        #         'files.file_name': { '$in': [
        #             'T7CNTC4_DBHOST2_version.csv', 
        #             'T7CNTC4_DBHOST2_options.csv', 
        #             'T7CNTC4_DBHOST2_dba_feature.csv'
        #         ] 
        #     } 
        # }, 
        #     collection=envs.MONGO_COLLECTION_ANALYSIS_NAME
        # )
        
        # self.assertGreater(len(stats_saved), 0)
        
        
        quota_saved = mongodata.fetch(
            match={
                'tenant_id': tenant_id,
                'uploader_id': uploader_id
            }, 
            collection=envs.MONGO_COLLECTION_UTILIZATION_NAME
        )
        
        self.assertGreater(len(quota_saved), 0)
        
        


