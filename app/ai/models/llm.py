"""
LLM Configuration

This module is responsible for creating and managing the application's
Language Model.

Every component should obtain the LLM instance from this module.
"""

from langchain_huggingface import ChatHuggingFace
from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import ConfigurationError, LLMError

logger = get_logger(__name__)

_llm: BaseChatModel | None = None


def initialize_llm() -> None:
    """
    Initialize the application's LLM.
    """

    global _llm

    if _llm is not None:
        logger.info("LLM already initialized.")
        return

    try:
        logger.info("Initializing Hugging Face LLM...")

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

    except Exception as e:
        logger.exception("Failed to initialize Hugging Face model.")

        raise LLMError("Unable to initialize the language model.") from e


def get_llm() -> BaseChatModel:
    """
    Return the initialized LLM.
    """

    if _llm is None:
        raise ConfigurationError("LLM has not been initialized.")

    return _llm