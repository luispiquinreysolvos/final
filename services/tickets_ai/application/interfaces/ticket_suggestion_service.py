from abc import ABC, abstractmethod

from application.dtos.suggest_ticket_response import SuggestTicketResponse
from domain.value_objects.ticket_images import TicketImages


class TicketSuggestionService(ABC):
    """Interface for suggesting ticket content."""

    @abstractmethod
    async def suggest_ticket(self, description: str, images: TicketImages | None = None) -> SuggestTicketResponse:
        """Suggest ticket content based on a problem description and optional images."""
        pass
