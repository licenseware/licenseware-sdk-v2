from dataclasses import dataclass



@dataclass(frozen=True)
class states:
    IDLE:str = 'idle'
    RUNNING:str = 'running'
    SUCCESS:str = 'success'
    FAILED:str = 'failed'
    TIMEOUT:str = 'timeout'
    SKIPPED:str = 'skipped'
    ACTION_REQUIRED:str = 'action_required'
    


