from dataclasses import dataclass


@dataclass(frozen=True)
class TicketTitle:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Ticket title is required")
