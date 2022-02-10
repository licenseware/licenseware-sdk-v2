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
    REQUEST_ACCEPTED:str = 'accepted'
    REQUEST_REJECTED:str = 'rejected'
    REQUEST_PENDING:str = 'pending'
    REQUEST_REQUESTED:str = 'requested'
    REQUEST_CANCELLED:str = 'cancelled'
    REQUEST_REVOKED:str = 'revoked'
    


