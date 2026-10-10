from abc import ABC, abstractmethod

from application.dtos.suggest_ticket_response import SuggestTicketResponse


class TicketSuggestionService(ABC):
    """Interface for suggesting ticket content."""

    @abstractmethod
    def suggest_ticket(self, description: str) -> SuggestTicketResponse:
        """Suggest ticket content based on a problem description."""
        pass
