from dataclasses import dataclass
from typing import List

from .report_component_type import ReportComponentType


@dataclass
class ReportType:
    app_id: str
    report_id: str
    name: str
    description: str
    flags: List[str]
    report_components: List[ReportComponentType]
    url: str
    public_url: str
    preview_image_url: str
    preview_image_dark_url: str
    connected_apps: List[str]
