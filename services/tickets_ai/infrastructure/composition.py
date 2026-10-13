from dataclasses import dataclass

from application.use_cases.suggest_ticket_with_ai import SuggestTicketWithAIUseCase
from application.interfaces.ticket_suggestion_service import TicketSuggestionService
from application.interfaces.ingest_tickets_into_vector_db_service import IngestTicketsIntoVectorDbService
from application.use_cases.ingest_tickets_into_vector_db import IngestTicketsIntoVectorDbUseCase
from presentation.controllers.ingest_ticket_into_vector_db_controller import IngestTicketIntoVectorDBController
from presentation.controllers.suggest_ticket_controller import SuggestTicketController


@dataclass
class Application:
    suggestion_service: TicketSuggestionService
    suggest_ticket_use_case: SuggestTicketWithAIUseCase
    ingest_tickets_into_vector_db_use_case: IngestTicketsIntoVectorDbUseCase

    @property
    def suggest_ticket_controller(self) -> SuggestTicketController:
        return SuggestTicketController(
            suggest_ticket_use_case=self.suggest_ticket_use_case,
        )

    @property
    def ingest_ticket_controller(self) -> IngestTicketIntoVectorDBController:
        return IngestTicketIntoVectorDBController(
            ingest_tickets_into_vector_db_use_case=self.ingest_tickets_into_vector_db_use_case,
        )


def create_application() -> Application:
    from infrastructure.ai.langchain_ollama_ticket_suggestion import LangChainOllamaTicketSuggestionService
    from infrastructure.ai.langchain_ollama_ticket_ingest import LangChainOllamaTicketIngest

    suggestion_service = LangChainOllamaTicketSuggestionService()
    ingest_service: IngestTicketsIntoVectorDbService = LangChainOllamaTicketIngest()
    return Application(
        suggestion_service=suggestion_service,
        suggest_ticket_use_case=SuggestTicketWithAIUseCase(
            suggestion_service=suggestion_service
        ),
        ingest_tickets_into_vector_db_use_case=IngestTicketsIntoVectorDbUseCase(
            ingest_tickets_into_vector_db_service=ingest_service
        ),
    )
