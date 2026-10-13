from dataclasses import dataclass


@dataclass(frozen= True)
class IngestTicketsIntoVectorDbResponse:
    id: int
    database: str
    company_id: int
    number: str | None
    name: str
    category: str | None
    partner_email: str | None
    team_id: int | None