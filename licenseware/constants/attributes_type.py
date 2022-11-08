from dataclasses import dataclass
from typing import Callable


@dataclass
class AttributesType:
    component_type: str
    metadata: dict
    attr: Callable
    attr_xaxis: Callable
    attr_yaxis: Callable
    attr_header: Callable
    attr_detail: Callable
    attr_series: Callable
    attr_categories: Callable
