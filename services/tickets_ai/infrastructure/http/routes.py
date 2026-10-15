import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile

from infrastructure.composition import Application
from infrastructure.http.rate_limit import limiter
from presentation.operation_result import OperationResult
from presentation.schemas.ingest_ticket_http_request import IngestTicketHttpRequest
from presentation.schemas.suggest_ticket_http_request import SuggestTicketHttpRequest
from presentation.schemas.suggest_ticket_http_response import SuggestTicketHttpResponse
from application.dtos.suggest_ticket_response import SuggestTicketResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_app(request: Request) -> Application:
    return request.app.state.container

@router.post(
    "/ingest",
    response_model=None,
    summary="Ingest ticket into vector DB",
)
async def ingest_ticket(
    payload: IngestTicketHttpRequest,
    request: Request,
    app: Application = Depends(get_app),
) -> None:
    client_host = request.client.host if request.client else "unknown"
    logger.info(
        "POST /tickets/ingest from %s",
        client_host,
        extra={"description_length": len(payload.description)},
    )
    result: OperationResult[None] = app.ingest_ticket_controller.handle(payload)
    if not result.is_success:
        logger.warning(
            "Ticket ingestion failed for %s: %s",
            client_host,
            result.error,
        )
        raise HTTPException(status_code=500, detail=str(result.error))
    logger.info(
        "Ticket ingestion succeeded for %s",
        client_host,
    )
    return None


@router.post(
    "/suggest",
    response_model=SuggestTicketHttpResponse,
    summary="Suggest ticket with AI",
)
@limiter.limit("10/minute")
async def suggest_ticket(
    problem_description: Annotated[str, Form(min_length=1)],
    request: Request,
    file: Annotated[list[UploadFile] | None, File()] = None,
    app: Application = Depends(get_app),
) -> SuggestTicketHttpResponse:
    payload = SuggestTicketHttpRequest(problem_description=problem_description)
    client_host = request.client.host if request.client else "unknown"
    logger.info(
        "POST /tickets/suggest from %s",
        client_host,
        extra={"description_length": len(payload.problem_description)},
    )

    result: OperationResult[SuggestTicketResponse] = await app.suggest_ticket_controller.handle(payload, file)
    if not result.is_success:
        logger.warning(
            "Ticket suggestion failed for %s: %s",
            client_host,
            result.error,
        )
        raise HTTPException(status_code=400, detail=result.error)

    logger.info(
        "Ticket suggestion succeeded for %s: title=%s, priority=%s",
        client_host,
        result.value.title,
        result.value.priority,
    )
    return result.value
