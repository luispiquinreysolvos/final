from datetime import datetime

from pydantic import BaseModel

from domain.value_objects.ticket_priority import TicketPriority


class IngestTicketHttpRequest(BaseModel):
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
