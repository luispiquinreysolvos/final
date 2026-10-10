from datetime import datetime

from domain.entities.ticket import Ticket
from domain.value_objects.ticket_description import TicketDescription
from domain.value_objects.ticket_email import TicketEmail
from domain.value_objects.ticket_number import TicketNumber
from domain.value_objects.ticket_priority import TicketPriority
from domain.value_objects.ticket_tags import TicketTags
from domain.value_objects.ticket_title import TicketTitle


class TicketFactory:
    @staticmethod
    def create(
        *,
        id: int,
        database: str,
        company_id: int,
        name: str,
        description: str,
        write_date: datetime,
        number: str | None = None,
        category: str | None = None,
        partner_email: str | None = None,
        tags: tuple[str, ...] = (),
        priority: TicketPriority = TicketPriority.MEDIUM,
        team_id: int | None = None,
        stage: str | None = None,
        closed: bool = False,
        active: bool = True,
    ) -> Ticket:
        return Ticket(
            id=id,
            database=database,
            company_id=company_id,
            number=TicketNumber(number) if number else None,
            name=TicketTitle(name),
            description=TicketDescription(description),
            category=category,
            partner_email=TicketEmail(partner_email),
            tags=TicketTags(tags),
            priority=priority,
            team_id=team_id,
            stage=stage,
            closed=closed,
            active=active,
            write_date=write_date,
        )
