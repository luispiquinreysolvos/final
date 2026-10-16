import logging
from dataclasses import dataclass

from application.dtos.ingest_tickets_into_vector_db_request import IngestTicketsIntoVectorDbRequest
from application.error import Error
from application.interfaces.ingest_tickets_into_vector_db_service import IngestTicketsIntoVectorDbService
from application.result import Result

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class IngestTicketsIntoVectorDbUseCase:
    """Stores a helpdesk ticket in the vector database so it can be retrieved as context."""
    ingest_tickets_into_vector_db_service: IngestTicketsIntoVectorDbService

    async def execute(self, ticket: IngestTicketsIntoVectorDbRequest) -> Result:
        if not ticket:
            logger.warning("Missing ticket in ingest use case")
            return Result.failure(Error.validation_error("Ticket is required"))

        logger.info(
            "Executing ingest ticket use case",
            extra={"ticket_id": ticket.id, "database": ticket.database},
        )

        response = await self.ingest_tickets_into_vector_db_service.ingest_tickets_into_vector_db(ticket)

        logger.info(
            "Use case completed successfully",
            extra={"ticket_id": ticket.id, "database": ticket.database},
        )
        return Result.success(response)
