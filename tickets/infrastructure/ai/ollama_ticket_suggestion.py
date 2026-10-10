import json
import os
from ollama import AsyncClient

from application.dtos.suggest_ticket_response import SuggestTicketResponse
from application.interfaces.ticket_suggestion_service import TicketSuggestionService


class OllamaTicketSuggestionService(TicketSuggestionService):
    def suggest_ticket(self, description: str) -> SuggestTicketResponse:
        pass