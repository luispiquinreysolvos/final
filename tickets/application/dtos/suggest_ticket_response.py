from dataclasses import dataclass


@dataclass(frozen=True)
class SuggestTicketResponse:
    title: str
    description: str
    priority: str
    tags: tuple[str, ...]
