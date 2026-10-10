from dataclasses import dataclass

from application.dtos.suggest_ticket_request import SuggestTicketRequest
from application.dtos.suggest_ticket_response import SuggestTicketResponse
from application.error import Error
from application.interfaces.ticket_suggestion_service import TicketSuggestionService
from application.result import Result

@dataclass(frozen=True)
class SuggestTicketWithAIUseCase:
    """Suggests ticket content using AI without creating the ticket automatically."""

    suggestion_service: TicketSuggestionService

    def execute(self, request: SuggestTicketRequest) -> Result:
        if not request.problem_description.strip():
            return Result.failure(Error.validation_error("Problem description is required"))

        response = self.suggestion_service.suggest_ticket(request.problem_description)
        return Result.success(response)
