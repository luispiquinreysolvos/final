from abc import ABC, abstractmethod

from application.dtos.ingest_tickets_into_vector_db_request import IngestTicketsIntoVectorDbRequest


class IngestTicketsIntoVectorDbService(ABC):

    @abstractmethod
    def ingest_tickets_into_vector_db(self, ticket: IngestTicketsIntoVectorDbRequest) -> None:
        pass
