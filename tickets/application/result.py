from dataclasses import dataclass
from typing import Any, Optional, Self

from application.error import Error


@dataclass(frozen=True)
class Result:
    """Represents success or failure of a use case execution."""

    value: Any = None
    error: Optional[Error] = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def success(cls, value: Any) -> Self:
        return cls(value=value)

    @classmethod
    def failure(cls, error: Error) -> Self:
        return cls(error=error)
