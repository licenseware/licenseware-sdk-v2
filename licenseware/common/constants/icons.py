from dataclasses import dataclass



@dataclass(frozen=True)
class icons:
    SERVERS:str = "ServersIcon"
    FEATURES:str = "FeaturesIcon"
    CPU:str = "CpuIcon"
    DATABASE_ROUNDED:str = "DatabaseIconRounded"
    DEVICE:str = "DeviceIcon"
    FILE:str = "FileIcon"
    
    