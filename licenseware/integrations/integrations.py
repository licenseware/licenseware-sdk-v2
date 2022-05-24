from dataclasses import dataclass


@dataclass(frozen=True)
class integrations:
    SERVICENOW: str = "servicenow"
    LANSWEEPER: str = "lansweeper"
