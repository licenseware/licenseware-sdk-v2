from licenseware.registry_service import register_upload_status
from licenseware.utils.logger import log
from licenseware.common.constants import envs


def notify_upload_status(event: dict, status:str):
    """
        Notify registry about uploader processing status
    """
    
    status = {
        'tenant_id': event['tenant_id'],
        'uploader_id': event['uploader_id'], 
        'status': status,
        'app_id': envs.APP_ID
    }
    
    response, status_code = register_upload_status(**status)
    
    if status_code != 200: return False
    return True