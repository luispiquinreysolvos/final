from dataclasses import dataclass, field

from domain.value_objects.ticket_images import TicketImages


@dataclass(frozen=True)
class SuggestTicketRequest:
    problem_description: str
    images: TicketImages = field(default_factory=TicketImages)

    def __post_init__(self) -> None:
        if not self.problem_description.strip():
            raise ValueError("Problem description is required")
