from licenseware.utils.logger import log
from licenseware.common.constants import states
from licenseware.notifications import notify_upload_status




def rv_tools_worker(event:dict):
    # This is the worker entrypoint  
    
    log.info("Starting working")
    notify_upload_status(event, status=states.RUNNING)
    
    # Here add the processing file logic
    # Worker logic doesn't have to be all in this function. 
    # You can create multiple sub-packages within this uploader package 
    
    log.debug(event) 
    
    
    notify_upload_status(event, status=states.IDLE)
    log.info("Finished working")
    