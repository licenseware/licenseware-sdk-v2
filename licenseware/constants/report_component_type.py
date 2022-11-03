from dataclasses import dataclass
from typing import List

from .attributes_type import AttributesType
from .report_filter_type import ReportFilterType
from .style_attributes_type import StyleAttrsType


@dataclass
class ReportComponentType:
    app_id: str
    title: str
    order: int
    component_id: str
    description: str
    url: str
    public_url: str
    style_attributes: StyleAttrsType
    attributes: AttributesType
    filters: List[ReportFilterType]
    type: str
