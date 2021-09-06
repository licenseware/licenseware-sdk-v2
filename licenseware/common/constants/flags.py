from dataclasses import dataclass



@dataclass(frozen=True)
class flags:
    BETA:str = 'beta'
    SOON:str = 'soon'


