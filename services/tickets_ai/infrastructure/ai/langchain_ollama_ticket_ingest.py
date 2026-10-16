import asyncio
import logging
import time
from dataclasses import dataclass, field

import chromadb

from application.dtos.ingest_tickets_into_vector_db_request import IngestTicketsIntoVectorDbRequest
from application.interfaces.ingest_tickets_into_vector_db_service import IngestTicketsIntoVectorDbService

logger = logging.getLogger(__name__)

COLLECTION_NAME = "tickets"


@dataclass
class LangChainOllamaTicketIngest(IngestTicketsIntoVectorDbService):
    ingestor: chromadb.Client = field(default_factory=lambda: chromadb.PersistentClient(path="./chroma_db"))
    collection: chromadb.Collection = field(init=False)

    def __post_init__(self) -> None:
        self.collection = self.ingestor.get_or_create_collection(
            name=COLLECTION_NAME
        )
        logger.info(
            "Initialized Chroma ingest service: collection=%s, documents=%d",
            COLLECTION_NAME,
            self.collection.count(),
        )

    async def ingest_tickets_into_vector_db(self, ticket: IngestTicketsIntoVectorDbRequest) -> None:
        logger.info(
            "Upserting ticket into vector DB",
            extra={
                "ticket_id": ticket.id,
                "database": ticket.database,
                "description_length": len(ticket.description),
            },
        )

        start_time = time.perf_counter()

        try:
            await asyncio.to_thread(
                self.collection.upsert,
                ids=[str(ticket.id)],
                documents=[ticket.description],
                metadatas=[{
                    "database": ticket.database,
                    "company_id": ticket.company_id,
                    "name": ticket.name,
                    "priority": ticket.priority.value,
                }],
            )
        except Exception as e:
            logger.error(
                "Vector DB upsert failed for ticket %s: %s",
                ticket.id,
                e,
                extra={"ticket_id": ticket.id, "database": ticket.database},
            )
            raise

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Ticket upserted into vector DB successfully",
            extra={
                "ticket_id": ticket.id,
                "database": ticket.database,
                "elapsed_ms": round(elapsed_ms, 2),
            },
        )
