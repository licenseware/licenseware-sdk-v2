import time
from functools import wraps

from licenseware import mongodata
from licenseware.common.constants import envs


def log_worker_processing_time(func):
    """
    Decorator for adding processing time for an uploader worker to History collection.

    Works on worker entrypoints for uploaders, relies on event_id to update the documents.

    Usage:
    @log_time
    def sccm_worker(event):
        do_work()

    """

    @wraps(func)
    def timeit_wrapper(event):
        start_time = time.perf_counter()
        result = func(event)
        total_time = time.perf_counter() - start_time
        mongodata.get_collection(envs.MONGO_COLLECTION_HISTORY_NAME).update_one(
            {"event_id": event["event_id"]},
            {
                "$set": {
                    "processing_time": time.strftime("%M:%S", time.gmtime(total_time))
                }
            },
        )
        return result

    return timeit_wrapper
