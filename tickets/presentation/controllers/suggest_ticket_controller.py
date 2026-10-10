from dataclasses import dataclass

from application.dtos.suggest_ticket_request import SuggestTicketRequest
from application.dtos.suggest_ticket_response import SuggestTicketResponse
from application.use_cases.suggest_ticket_with_ai import SuggestTicketWithAIUseCase
from presentation.operation_result import OperationResult
from presentation.schemas.suggest_ticket_http_request import SuggestTicketHttpRequest


@dataclass
class SuggestTicketController:
    suggest_ticket_use_case: SuggestTicketWithAIUseCase

    def handle(self, http_request: SuggestTicketHttpRequest) -> OperationResult[SuggestTicketResponse]:
        try:
            request = SuggestTicketRequest(problem_description=http_request.problem_description)
            result = self.suggest_ticket_use_case.execute(request)
        except ValueError as error:
            return OperationResult.fail(str(error))

        if result.error is not None:
            return OperationResult.fail(result.error.message)

        return OperationResult.succeed(result.value)