from dataclasses import dataclass, asdict
from typing import List


@dataclass
class WorkerEvent:
    tenant_id: str
    authorization: str
    uploader_id: str
    uploader_name: str
    event_id: str
    app_id: str
    app_name: str
    filepaths: List[str]
    clear_data: bool = False
    event_type: str = "ProcessingDetails"

    def dict(self):
        return asdict(self)
