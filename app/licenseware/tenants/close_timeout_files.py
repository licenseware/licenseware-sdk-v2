import datetime
import app.licenseware.mongodata as m
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs


#TODO close timeout files for tenant_id

def close_timed_out_files(analysis_collection_name:str = None):
    
    time_out_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
    start_time = datetime.datetime.utcnow() - datetime.timedelta(days=360)

    
    _filter = {'files.status': {"$eq": 'Running'},
                'files.analysis_date': {'$gt': start_time.isoformat(), '$lt': time_out_time.isoformat()}}

    stats_collection = m.get_collection(analysis_collection_name or envs.MONGO_ANALYSIS_NAME)

    update_data = {
        '$set': {
            'files.$[file].status': 'Timeout'
        }
    }
    
    timed_out = stats_collection.update_many(
        filter=_filter,
        update=update_data,
        upsert=False,
        array_filters=[{"file.status": {"$eq": 'Running'},
                        'file.analysis_date': {
                            '$gt': start_time.isoformat(),
                            '$lt': time_out_time.isoformat()
        }}]
    )
    
    log.warning(timed_out.matched_count)
    
    if timed_out.matched_count > 0:
        return timed_out
    
    
    _filter = {
        'status': 'Running',
        'updated_at': {
            '$gt': start_time.isoformat(),
            '$lt': time_out_time.isoformat()
        }
    }

    update_data = {
        '$set': {
            'status': 'Timeout'
        }
    }
    
    return stats_collection.update_many(filter=_filter, upsert=False, update=update_data)

