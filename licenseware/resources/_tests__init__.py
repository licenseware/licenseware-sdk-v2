from dotenv import load_dotenv
load_dotenv()  

import os, io
from werkzeug.datastructures import FileStorage
from licenseware.utils.logger import log


tenant_id = '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'
 
headers = {
    'Tenantid': tenant_id,
    'Authorization': 'TheAuthorization' 
}



def get_mock_binary_files(files_path:str):
    
    
    mock_binary_files = []
    for fname in os.listdir(files_path):
        
        fpath = os.path.join(files_path, fname)
        
        if not os.path.isfile(fpath): 
            log.warning(f"'{fpath}' is not a file skipped")
            continue
        
        with open(fpath, 'rb') as f:
            file_binary = io.BytesIO(f.read())
        
        mock_file = FileStorage(
            stream = file_binary,
            filename = fname,
            content_type = "application/*",
        )
        
        mock_binary_files.append((mock_file, fname)) 

    return {'files[]': mock_binary_files}



def mock_event(uploader_id:str, valid_filepaths:list):
    
    valid_filepaths = [os.path.abspath(fpath) for fpath in valid_filepaths]
    
    event = {
        'tenant_id': tenant_id,
        'uploader_id': uploader_id,
        'filepaths': valid_filepaths, 
        'flask_request':  {},
        'validation_response': {}
    }
    
    return event




uploader_event_example = {'tenant_id': '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a',
 'uploader_id': 'review_lite',
 'filepaths': ['/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/anjin_SD2213_version.csv',
  '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/anjin_SD2213_dba_feature.csv',
  '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/anjin_SD2213_options.csv'],
 'flask_request': {'User-Agent': 'werkzeug/1.0.1',
  'Host': 'localhost',
  'Content-Type': 'multipart/form-data; boundary="---------------WerkzeugFormPart_1631530283.73436260.7204684218275901"',
  'Content-Length': '511426',
  'Tenantid': '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a',
  'Authorization': 'TheAuthorization'},
 'validation_response': {'tenant_id': '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a',
  'status': 'success',
  'message': 'Files are valid',
  'validation': [{'status': 'success',
    'filename': 'anjin_SD2213_version.csv',
    'filepath': '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/anjin_SD2213_version.csv',
    'message': 'Filename is valid'},
   {'status': 'success',
    'filename': 'anjin_SD2213_dba_feature.csv',
    'filepath': '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/anjin_SD2213_dba_feature.csv',
    'message': 'Filename is valid'},
   {'status': 'success',
    'filename': 'anjin_SD2213_options.csv',
    'filepath': '/tmp/lware/3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a/anjin_SD2213_options.csv',
    'message': 'Filename is valid'}]}}