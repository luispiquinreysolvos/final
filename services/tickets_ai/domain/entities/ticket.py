from dataclasses import dataclass, field
from datetime import datetime

from domain.value_objects.ticket_description import TicketDescription
from domain.value_objects.ticket_email import TicketEmail
from domain.value_objects.ticket_images import TicketImages
from domain.value_objects.ticket_number import TicketNumber
from domain.value_objects.ticket_priority import TicketPriority
from domain.value_objects.ticket_tags import TicketTags
from domain.value_objects.ticket_title import TicketTitle


@dataclass
class Ticket:
    id: int
    database: str  # Source Odoo database; scopes ticket and company IDs to their origin.
    company_id: int
    number: TicketNumber | None
    name: TicketTitle
    description: TicketDescription
    category: str | None
    partner_email: TicketEmail | None
    tags: TicketTags
    priority: TicketPriority
    team_id: int | None
    stage: str | None
    closed: bool
    active: bool
    write_date: datetime
    images: TicketImages = field(default_factory=TicketImages)

    def is_searchable(self) -> bool:
        return self.active

    def can_be_used_as_closed_reference(self) -> bool:
        return self.is_searchable() and self.closed
