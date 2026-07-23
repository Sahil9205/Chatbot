"""
Hugging Face Embedding Model

Implementation of BaseEmbeddingModel using
Sentence Transformers.
"""

from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.core.logging import get_logger

from .base import BaseEmbeddingModel


logger = get_logger(__name__)


class HuggingFaceEmbeddingModel(BaseEmbeddingModel):
    """
    Hugging Face implementation of the embedding model.
    """

    def __init__(self) -> None:

        logger.info("Loading embedding model: %s",settings.EMBEDDING_MODEL_NAME,)

        self._model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME )

        logger.info("Embedding model loaded successfully.")

    @property
    def model_name(self) -> str:
        """
        Return the model name.
        """
        return settings.EMBEDDING_MODEL_NAME

    @property
    def embedding_dimension(self) -> int:
        """
        Return embedding dimension.
        """
        return self._model.get_sentence_embedding_dimension()

    def embed_text(self,text: str,) -> list[float]:
        """
        Generate embedding for one text.
        """

        return self._model.encode(text,normalize_embeddings=True,).tolist()

    def embed_documents(self,texts: list[str],) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        return self._model.encode(texts,normalize_embeddings=True, ).tolist()

    
    def embed_query(self,query: str,) -> list[float]:
        """
        Generate embedding for a search query.
        """

        logger.info("Generating embedding for search query.")

        embedding = self._model.encode(query,normalize_embeddings=True,).tolist()

        logger.info("Successfully generated query embedding.")

        return embedding