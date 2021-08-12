from dataclasses import dataclass



@dataclass
class quotas:
    
    CPUQ:int = 10 # Databases
    RV_TOOLS:int = 1 # Files
    LMS_DETAIL:int = 1 # Files
    




QUOTA = {
    #IFMP
    "cpuq": 10,  # Databases
    "rv_tools": 1,  # Files
    "lms_detail": 1,  # Files
    "powercli": 1,  # Files
    
    #ODB
    "review_lite": 16, # Databases
    "lms_options": 1, # Files

    #OFMW
    "ofmw_archive": 1,  # 1 Device  == 1 archive
    
    #CM
    "pdf_contract": 1, # 1 pdf contract
    
    #MDM
    "sccm_queries": 1 # 1 pack of 3 csv files
}


if os.getenv('DEBUG') == 'true':
    QUOTA = dict(
        zip(QUOTA.keys(), [sys.maxsize]*len(QUOTA.keys()))
    )