from dataclasses import dataclass, field

import chromadb

from application.dtos.ingest_tickets_into_vector_db_request import IngestTicketsIntoVectorDbRequest
from application.interfaces.ingest_tickets_into_vector_db_service import IngestTicketsIntoVectorDbService

@dataclass
class LangChainOllamaTicketIngest(IngestTicketsIntoVectorDbService):
    ingestor: chromadb.Client = field(default_factory=lambda: chromadb.PersistentClient(path="./chroma_db"))
    collection: chromadb.Collection = field(init=False)

    def __post_init__(self) -> None:
        self.collection = self.ingestor.get_or_create_collection(
            name="tickets"
        )

    def ingest_tickets_into_vector_db(self, ticket: IngestTicketsIntoVectorDbRequest) -> None:
        self.collection.upsert(
            ids=[str(ticket.id)],
            documents=[ticket.description],
            metadatas=[{
                "database": ticket.database,
                "company_id": ticket.company_id,
                "name": ticket.name,
                "priority": ticket.priority.value,
            }],
        )
