from dataclasses import dataclass


@dataclass(frozen=True)
class TicketNumber:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Ticket number cannot be empty")
