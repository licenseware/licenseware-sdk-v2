import app.licenseware.mongodata as m
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from .close_timeout_files import close_timed_out_files




def get_processing_status(tenant_id:str, analysis_collection_name:str = None):
    """
        Get processing status for a tenant_id from all uploaders
    """
    
    close_timed_out_files()

    query = {
        'tenant_id': tenant_id, 
        '$or': [
            {
                'files.status': 'Running'
            },
            {
                'status': 'Running'
            }
    ]}
    
    results = m.document_count(
        match=query, 
        collection=analysis_collection_name or envs.MONGO_ANALYSIS_NAME
    )
    
    log.info(results)

    if results > 0:
        return {'status': 'Running'}, 200
    return {'status': 'Idle'}, 200




def get_uploader_status(tenant_id:str, uploader_id:str, analysis_collection_name:str = None):
    """
        Get processing status for a tenant_id and the specified uploader
    """

    close_timed_out_files()

    query = {
        'tenant_id': tenant_id,
        'file_type': uploader_id,
        '$or': [
            {
                'files.status': 'Running'
            },
            {
                'status': 'Running'
            }
        ]
    }

    results = m.document_count(
        match=query, 
        collection=analysis_collection_name or envs.MONGO_ANALYSIS_NAME
    )
    
    log.info(results)

    if results > 0:
        return {'status': 'Running'}, 200
    return {'status': 'Idle'}, 200