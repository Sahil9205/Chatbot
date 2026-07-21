"""
LLM Configuration

This module is responsible for creating and managing the application's
Language Model.

Every component should obtain the LLM instance from this module.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_huggingface import ChatHuggingFace

from app.core.config import settings
from app.core.exceptions import ConfigurationError, LLMError
from app.core.logging import get_logger

logger = get_logger(__name__)

_llm: BaseChatModel | None = None


def initialize_llm() -> None:
    """
    Initialize the application's Language Model.

    The model is initialized only once during the application's
    lifetime. Subsequent calls return immediately.

    Raises
    ------
    ConfigurationError
        If the required LLM configuration is missing.

    LLMError
        If the language model fails to initialize.
    """

    global _llm

    if _llm is not None:
        logger.info("LLM is already initialized.")
        return

    if not settings.LLM_MODEL_NAME:
        logger.error("LLM_MODEL_NAME is not configured.")
        raise ConfigurationError(
            "LLM_MODEL_NAME is not configured."
        )

    if not settings.HUGGINGFACE_API_KEY:
        logger.error("HUGGINGFACE_API_KEY is not configured.")
        raise ConfigurationError(
            "HUGGINGFACE_API_KEY is not configured."
        )

    try:
        logger.info(
            "Initializing Hugging Face model: %s",
            settings.LLM_MODEL_NAME,
        )

        _llm = ChatHuggingFace(
            repo_id=settings.LLM_MODEL_NAME,
            huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY,
            temperature=settings.TEMPERATURE,
            max_new_tokens=settings.MAX_NEW_TOKENS,
        )

        logger.info(
            "Successfully initialized model: %s",
            settings.LLM_MODEL_NAME,
        )

    except Exception as exc:
        logger.exception("Failed to initialize Hugging Face model.")

        raise LLMError(
            "Unable to initialize the language model."
        ) from exc


def get_llm() -> BaseChatModel:
    """
    Return the initialized Language Model.

    Returns
    -------
    BaseChatModel
        The application's initialized language model.

    Raises
    ------
    ConfigurationError
        If the language model has not been initialized.
    """

    if _llm is None:
        logger.error(
            "Attempted to access the LLM before initialization."
        )

        raise ConfigurationError(
            "LLM has not been initialized."
        )

    return _llm