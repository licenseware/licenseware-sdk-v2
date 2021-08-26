"""

Here define app ids and their uploaders_ids along with uploader_ids max quota.

Each item in `QUOTA` dictionary has the following shape:

```js
'app_id': {
    "uploader_id1": set_quota(10),  # Databases
    "uploader_id2": set_quota(1),  # Files
    "uploader_id_etc": set_quota(1),  # Files
}
```

**Atention!** 
`APP_ID` from .env file should be present in `QUOTA` dictionary


"""


import sys
from .envs import envs

# If debug true remove limit 
max_int = sys.maxsize
set_quota = lambda q: max_int if envs.DEBUG else q



QUOTA = {
    
    'ifmp': {
        "cpuq": set_quota(10),  # Databases
        "rv_tools": set_quota(1),  # Files
        "lms_detail": set_quota(1),  # Files
        "powercli": set_quota(1),  # Files        
    },
    
    'odb': {
        "review_lite": set_quota(16), # Databases
        "lms_options": set_quota(1), # Files
    },
    
    'fmw': {
        "fmw_archive": set_quota(1),  # 1 Device  == 1 archive
    },
    
    'contracts': {
        "pdf_contract": set_quota(1), # 1 pdf contract
    },
    
    'mdm': {
        "sccm_queries": set_quota(1) # 1 pack of 3 csv files    
    }
    
}

# Selecting uploader_ids for current app
QUOTA = QUOTA[envs.APP_ID]


 