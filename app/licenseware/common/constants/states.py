from dataclasses import dataclass



@dataclass(frozen=True)
class states:
    IDLE:str = 'idle'
    RUNNING:str = 'running'
    SUCCESS:str = 'success'
    FAIL:str = 'fail'


