from fastapi import APIRouter, Depends, HTTPException

from infrastructure.composition import Application, create_application
from presentation.operation_result import OperationResult
from presentation.schemas.suggest_ticket_http_request import SuggestTicketHttpRequest
from application.dtos.suggest_ticket_response import SuggestTicketResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_app() -> Application:
    return create_application()


@router.post(
    "/suggest",
    response_model=SuggestTicketResponse,
    summary="Suggest ticket with AI",
)
async def suggest_ticket(
    payload: SuggestTicketHttpRequest,
    app: Application = Depends(get_app),
) -> SuggestTicketResponse:
    result: OperationResult[SuggestTicketResponse] = app.suggest_ticket_controller.handle(payload)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.value