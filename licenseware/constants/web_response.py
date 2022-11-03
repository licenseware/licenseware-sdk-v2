from dataclasses import dataclass
from typing import Any


@dataclass
class WebResponse:
    content: Any
    status_code: int
