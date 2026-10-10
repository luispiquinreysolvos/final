from dataclasses import dataclass

from application.use_cases.suggest_ticket_with_ai import SuggestTicketWithAIUseCase
from application.interfaces.ticket_suggestion_service import TicketSuggestionService
from presentation.controllers.suggest_ticket_controller import SuggestTicketController


@dataclass
class Application:
    suggestion_service: TicketSuggestionService
    suggest_ticket_use_case: SuggestTicketWithAIUseCase

    @property
    def suggest_ticket_controller(self) -> SuggestTicketController:
        return SuggestTicketController(
            suggest_ticket_use_case=self.suggest_ticket_use_case,
        )

def create_application() -> Application:
    from infrastructure.ai.ollama_ticket_suggestion import OllamaTicketSuggestionService

    suggestion_service = OllamaTicketSuggestionService()
    return Application(
        suggestion_service=suggestion_service,
        suggest_ticket_use_case=SuggestTicketWithAIUseCase(
            suggestion_service=suggestion_service
        ),
    )