"""
Session Router.

Provides session management endpoints.
"""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_session_service
from app.api.schemas.session_response import SessionResponse

from app.conversation.session_service import SessionService


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post(
    "",
    response_model=SessionResponse,
)
def create_session(
    session_service: SessionService = Depends(
        get_session_service,
    ),
) -> SessionResponse:
    """
    Create a new chat session.
    """

    session = session_service.create_session()

    return SessionResponse(
        session_id=session.session_id,
    )