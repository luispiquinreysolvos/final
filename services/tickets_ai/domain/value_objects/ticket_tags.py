from dataclasses import dataclass


@dataclass(frozen=True)
class TicketTags:
    values: tuple[str, ...]

    def __post_init__(self) -> None:
        if any(not tag.strip() for tag in self.values):
            raise ValueError("Ticket tags cannot be empty")
