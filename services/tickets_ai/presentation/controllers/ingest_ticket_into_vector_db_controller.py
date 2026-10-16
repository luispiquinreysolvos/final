import logging
from dataclasses import dataclass

from application.dtos.ingest_tickets_into_vector_db_request import IngestTicketsIntoVectorDbRequest
from application.use_cases.ingest_tickets_into_vector_db import IngestTicketsIntoVectorDbUseCase
from presentation.operation_result import OperationResult
from presentation.schemas.ingest_ticket_http_request import IngestTicketHttpRequest

logger = logging.getLogger(__name__)


@dataclass
class IngestTicketIntoVectorDBController:
    ingest_tickets_into_vector_db_use_case: IngestTicketsIntoVectorDbUseCase

    async def handle(
        self, http_request: IngestTicketHttpRequest
    ) -> OperationResult[None]:
        logger.info(
            "Handling ticket ingestion request",
            extra={"ticket_id": http_request.id, "database": http_request.database},
        )

        try:
            request = IngestTicketsIntoVectorDbRequest(
                id=http_request.id,
                database=http_request.database,
                company_id=http_request.company_id,
                number=http_request.number,
                name=http_request.name,
                description=http_request.description,
                category=http_request.category,
                partner_email=http_request.partner_email,
                tags=http_request.tags,
                priority=http_request.priority,
                team_id=http_request.team_id,
                stage=http_request.stage,
                closed=http_request.closed,
                active=http_request.active,
                write_date=http_request.write_date,
            )
            result = await self.ingest_tickets_into_vector_db_use_case.execute(request)
        except ValueError as error:
            logger.warning("Invalid ingestion request: %s", error)
            return OperationResult.fail(str(error))

        if result.error is not None:
            logger.warning(
                "Use case returned error: %s (code: %s)",
                result.error.message,
                result.error.code.name,
            )
            return OperationResult.fail(result.error.message)

        logger.info(
            "Ticket ingestion completed successfully",
            extra={"ticket_id": request.id, "database": request.database},
        )
        return OperationResult.succeed(None)
