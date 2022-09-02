import datetime

from licenseware import mongodata as m
from licenseware.common.constants import envs, states
from licenseware.utils.logger import log

#! OUTDATED


def close_timed_out_files():

    time_out_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
    start_time = datetime.datetime.utcnow() - datetime.timedelta(days=360)

    _filter = {
        "files.status": {"$eq": states.RUNNING},
        "files.analysis_date": {
            "$gt": start_time.isoformat(),
            "$lt": time_out_time.isoformat(),
        },
    }

    stats_collection = m.get_collection(envs.MONGO_COLLECTION_ANALYSIS_NAME)

    update_data = {"$set": {"files.$[file].status": states.TIMEOUT}}

    timed_out = stats_collection.update_many(
        filter=_filter,
        update=update_data,
        upsert=False,
        array_filters=[
            {
                "file.status": {"$eq": states.RUNNING},
                "file.analysis_date": {
                    "$gt": start_time.isoformat(),
                    "$lt": time_out_time.isoformat(),
                },
            }
        ],
    )

    log.info(timed_out.matched_count)

    if timed_out.matched_count > 0:
        return timed_out

    _filter = {
        "status": states.RUNNING,
        "updated_at": {"$gt": start_time.isoformat(), "$lt": time_out_time.isoformat()},
    }

    update_data = {"$set": {"status": states.TIMEOUT}}

    return stats_collection.update_many(
        filter=_filter, upsert=False, update=update_data
    )
