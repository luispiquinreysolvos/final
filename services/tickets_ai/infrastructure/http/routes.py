import logging
from fastapi import APIRouter, Depends, HTTPException, Request

from infrastructure.composition import Application
from presentation.operation_result import OperationResult
from presentation.schemas.suggest_ticket_http_request import SuggestTicketHttpRequest
from presentation.schemas.suggest_ticket_http_response import SuggestTicketHttpResponse
from application.dtos.suggest_ticket_response import SuggestTicketResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_app(request: Request) -> Application:
    return request.app.state.container


@router.post(
    "/suggest",
    response_model=SuggestTicketHttpResponse,
    summary="Suggest ticket with AI",
)
async def suggest_ticket(
    payload: SuggestTicketHttpRequest,
    request: Request,
    app: Application = Depends(get_app),
) -> SuggestTicketHttpResponse:
    client_host = request.client.host if request.client else "unknown"
    logger.info(
        "POST /tickets/suggest from %s",
        client_host,
        extra={"description_length": len(payload.problem_description)},
    )

    result: OperationResult[SuggestTicketResponse] = app.suggest_ticket_controller.handle(payload)
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
