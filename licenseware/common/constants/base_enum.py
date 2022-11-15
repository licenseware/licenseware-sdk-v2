from enum import Enum


class BaseEnum(str, Enum):  # pragma: no cover
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"'{self._value_}'"
