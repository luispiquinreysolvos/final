from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class OperationResult(Generic[T]):
    value: T | None = None
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.error is None

    @classmethod
    def succeed(cls, value: T) -> "OperationResult[T]":
        return cls(value=value)

    @classmethod
    def fail(cls, error: str) -> "OperationResult[T]":
        return cls(error=error)