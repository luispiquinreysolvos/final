from dataclasses import dataclass

from application.dtos.ingest_tickets_into_vector_db_request import IngestTicketsIntoVectorDbRequest
from application.interfaces.ingest_tickets_into_vector_db_service import IngestTicketsIntoVectorDbService
from application.result import Result


@dataclass(frozen=True)
class IngestTicketsIntoVectorDbUseCase:
    ingest_tickets_into_vector_db_service: IngestTicketsIntoVectorDbService

    def execute(self, ticket: IngestTicketsIntoVectorDbRequest) -> Result:
        self.ingest_tickets_into_vector_db_service.ingest_tickets_into_vector_db(ticket)