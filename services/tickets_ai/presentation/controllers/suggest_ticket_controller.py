import logging
from dataclasses import dataclass

from application.dtos.suggest_ticket_request import SuggestTicketRequest
from application.dtos.suggest_ticket_response import SuggestTicketResponse
from application.use_cases.suggest_ticket_with_ai import SuggestTicketWithAIUseCase
from presentation.operation_result import OperationResult
from presentation.schemas.suggest_ticket_http_request import SuggestTicketHttpRequest

logger = logging.getLogger(__name__)


@dataclass
class SuggestTicketController:
    suggest_ticket_use_case: SuggestTicketWithAIUseCase

    def handle(self, http_request: SuggestTicketHttpRequest) -> OperationResult[SuggestTicketResponse]:
        logger.info(
            "Handling ticket suggestion request",
            extra={"description_length": len(http_request.problem_description)},
        )

        try:
            request = SuggestTicketRequest(problem_description=http_request.problem_description)
            result = self.suggest_ticket_use_case.execute(request)
        except ValueError as error:
            logger.warning("Invalid request: %s", error)
            return OperationResult.fail(str(error))

        if result.error is not None:
            logger.warning(
                "Use case returned error: %s (code: %s)",
                result.error.message,
                result.error.code.name,
            )
            return OperationResult.fail(result.error.message)

        logger.info(
            "Ticket suggestion completed successfully",
            extra={"title": result.value.title, "priority": result.value.priority},
        )
        return OperationResult.succeed(result.value)