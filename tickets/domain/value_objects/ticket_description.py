from dataclasses import dataclass


@dataclass(frozen=True)
class TicketDescription:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Ticket description is required")
