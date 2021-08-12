import app.licenseware.mongodata as m
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs



def get_activated_tenants(tenant_id:str = None, utilization_collection_name:str = None):
    """
        Retreive from mongo Utilization collection tenants that activated one or more apps 
    """
    
    if not tenant_id:
        tenants_list = m.fetch(
            match='tenant_id', collection=utilization_collection_name or envs.MONGO_UTILIZATION_NAME
        )
        log.info(f"Activated_tenants: {tenants_list}")
        return tenants_list

    tenants_list = m.fetch(
        match={'tenant_id': tenant_id}, collection=utilization_collection_name or envs.MONGO_UTILIZATION_NAME
    )
    log.info(f"Activated tenant: {tenants_list}")
    
    return tenants_list


def get_last_update_dates(tenant_id:str = None, data_collection_name:str = None):
    
    pipeline = [
        {
            '$group': {
                '_id': {
                    'tenant_id': '$tenant_id'
                },
                'last_update_date': {
                    '$max': '$updated_at'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'tenant_id': '$_id.tenant_id',
                'last_update_date': '$last_update_date'
            }
        }
    ]

    if tenant_id:
        pipeline.insert(0, {'$match': {'tenant_id': tenant_id}})

    last_update_dates = m.aggregate(
        pipeline, 
        collection = data_collection_name or envs.MONGO_DATA_NAME
    )

    if not last_update_dates:
        log.info("Could not get last update dates")

    return last_update_dates


def get_tenants_with_data(tenant_id=None, data_collection_name:str = None):    
    """
        Retreive from mongo Data collection tenants that processed files on one or more apps  
    """

    enabled_tenants = get_last_update_dates(tenant_id, data_collection_name)

    if enabled_tenants:
        enabled_tenants = [{
            "tenant_id": tenant["tenant_id"],
            "last_update_date": tenant["last_update_date"]
        } for tenant in enabled_tenants]

    log.info(f"enabled_tenants: {enabled_tenants}")
    return enabled_tenants



def clear_tenant_data(tenant_id, data_collection_name:str = None):

    res = m.delete(
        match={'tenant_id': tenant_id},
        collection=data_collection_name or envs.MONGO_DATA_NAME 
    )

    log.info(f"tenant data deleted: {res}")
