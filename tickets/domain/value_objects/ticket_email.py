from dataclasses import dataclass
from re import fullmatch


@dataclass(frozen=True)
class TicketEmail:
    value: str | None

    def __post_init__(self) -> None:
        if self.value and not fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", self.value):
            raise ValueError("Invalid ticket email")
