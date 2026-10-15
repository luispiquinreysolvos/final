from dataclasses import dataclass, field

from domain.value_objects.ticket_image import Image


@dataclass(frozen=True)
class TicketImages:
    images: list[Image] = field(default_factory=list)
