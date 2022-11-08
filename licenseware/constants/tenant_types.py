from dataclasses import dataclass
from typing import List


@dataclass
class TenantRegistrationResponse:
    app_activated: bool
    data_available: bool
    tenants_with_public_reports: List[str]
    last_update_date: str
