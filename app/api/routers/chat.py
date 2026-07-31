"""
Chat Router.

Provides chat endpoints.
"""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat_service
from app.api.schemas.chat_request import ChatRequest
from app.api.schemas.chat_response import ChatResponse

from app.chat.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(
        get_chat_service,
    ),
) -> ChatResponse:
    """
    Process a chat request.
    """

    return chat_service.chat(
        request,
    )