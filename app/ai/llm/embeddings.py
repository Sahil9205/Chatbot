"""
Embedding Model Configuration

This module is responsible for creating and managing the application's
embedding model.

The embedding model is used to convert text into dense vectors for
semantic search in the vector database.

Every component should obtain the embedding model from this module.
"""

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings
from app.core.exceptions import ConfigurationError, EmbeddingError
from app.core.logging import get_logger

logger = get_logger(__name__)

_embedding_model: Embeddings | None = None


def initialize_embeddings() -> None:
    """
    Initialize the embedding model.

    This function should be called once during application startup.
    """

    global _embedding_model

    if _embedding_model is not None:
        logger.info("Embedding model already initialized.")
        return

    try:
        logger.info(
            "Initializing embedding model: %s",
            settings.EMBEDDING_MODEL_NAME,
        )

        _embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
            model_kwargs={"device": settings.EMBEDDING_DEVICE},
            
            encode_kwargs={"normalize_embeddings": True,},
        )

        logger.info("Embedding model initialized successfully.")

    except Exception as e:
        logger.exception("Failed to initialize embedding model.")

        raise EmbeddingError("Unable to initialize embedding model.") from e


def get_embeddings() -> Embeddings:
    """
    Return the initialized embedding model.

    Raises
    ------
    ConfigurationError
        If the embedding model has not been initialized.
    """

    if _embedding_model is None:
        raise ConfigurationError("Embedding model has not been initialized.")

    return _embedding_model