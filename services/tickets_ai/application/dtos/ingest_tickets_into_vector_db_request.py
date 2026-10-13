import datetime
from dataclasses import dataclass

from domain.value_objects.ticket_priority import TicketPriority

@dataclass(frozen= True)
class IngestTicketsIntoVectorDbRequest:
    id: int
    database: str
    company_id: int
    number: str | None
    name: str
    description: str
    category: str | None
    partner_email: str | None
    tags: tuple[str, ...]
    priority: TicketPriority
    team_id: int | None
    stage: str | None
    closed: bool
    active: bool
    write_date: datetime

    def __post_init__(self) -> None:
        if self.id <= 0:
            raise ValueError("Ticket ID must be positive")
        if not self.database.strip():
            raise ValueError("Database is required")
        if self.company_id <= 0:
            raise ValueError("Company ID must be positive")
        if not self.name.strip():
            raise ValueError("Ticket name is required")
        if not isinstance(self.write_date, datetime.datetime):
            raise ValueError("Write date must be a datetime")


