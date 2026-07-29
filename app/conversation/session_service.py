"""
Session Service.

Responsible for managing chat sessions.
"""

from datetime import UTC, datetime

from app.core.exceptions import SessionNotFoundError
from app.core.logging import get_logger

from .conversation_service import ConversationService
from .schemas.session import Session



logger = get_logger(__name__)


class SessionService:
    """
    Manages chat sessions.

    A session is mapped to exactly one conversation.
    """

    def __init__(
        self,
        conversation_service: ConversationService,
    ) -> None:
        """
        Parameters
        ----------
        conversation_service : ConversationService
        """

        self.conversation_service = conversation_service

        self._sessions: dict[str, Session] = {}

    ####################################################################
    # Public Methods
    ####################################################################

    def create_session(self) -> Session:
        """
        Create a new session and its conversation.

        Returns
        -------
        Session
        """

        conversation = (
            self.conversation_service.create_conversation()
        )

        session = Session(
            conversation_id=conversation.conversation_id,
        )

        self._sessions[
            session.session_id
        ] = session

        logger.info(
            "Created session '%s'.",
            session.session_id,
        )

        return session

    def get_session(
        self,
        session_id: str,
    ) -> Session:
        """
        Retrieve a session.

        Parameters
        ----------
        session_id : str

        Returns
        -------
        Session

        Raises
        ------
        SessionNotFoundError
        """

        session = self._sessions.get(
            session_id
        )

        if session is None:

            logger.warning(
                "Session '%s' not found.",
                session_id,
            )

            raise SessionNotFoundError(
                f"Session '{session_id}' does not exist."
            )

        return session

    def get_conversation_id(
        self,
        session_id: str,
    ) -> str:
        """
        Return the conversation ID
        associated with a session.
        """

        session = self.get_session(
            session_id
        )

        session.updated_at = datetime.now(
            UTC
        )

        return session.conversation_id

    def delete_session(
        self,
        session_id: str,
    ) -> None:
        """
        Delete a session and its conversation.
        """

        session = self.get_session(
            session_id
        )

        self.conversation_service.delete_conversation(
            session.conversation_id
        )

        del self._sessions[
            session_id
        ]

        logger.info("Deleted session '%s'.",session_id,)