from dataclasses import dataclass
from enum import Enum
from typing import Self


class ErrorCode(Enum):
    # Add error codes here as new application error cases are identified.
    VALIDATION_ERROR = "VALIDATION_ERROR"

@dataclass(frozen=True)
class Error:
    """
    Domain errors describe violated business rules; this type translates them
    into stable outcomes that use cases and outer layers can handle consistently.
    The Application layer orchestrates domain behavior and shapes its outcomes,
    without moving business rules out of the Domain layer.
    """
    code : ErrorCode
    message :  str

    @classmethod
    def validation_error(cls, message: str) -> Self:
        return cls (
            code = ErrorCode.VALIDATION_ERROR,
            message = message
        )
