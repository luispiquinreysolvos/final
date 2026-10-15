import logging
from dataclasses import dataclass

from application.dtos.suggest_ticket_request import SuggestTicketRequest
from application.dtos.suggest_ticket_response import SuggestTicketResponse
from application.error import Error
from application.interfaces.ticket_suggestion_service import TicketSuggestionService
from application.result import Result

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SuggestTicketWithAIUseCase:
    """Suggests ticket content using AI without creating the ticket automatically."""
    suggestion_service: TicketSuggestionService

    async def execute(self, request: SuggestTicketRequest) -> Result:
        logger.info(
            "Executing suggest ticket use case",
            extra={"description_length": len(request.problem_description)},
        )

        if not request.problem_description.strip():
            logger.warning("Empty problem description in use case")
            return Result.failure(Error.validation_error("Problem description is required"))

        response = await self.suggestion_service.suggest_ticket(request.problem_description, request.images)

        logger.info(
            "Use case completed successfully",
            extra={"title": response.title, "priority": response.priority},
        )
        return Result.success(response)
