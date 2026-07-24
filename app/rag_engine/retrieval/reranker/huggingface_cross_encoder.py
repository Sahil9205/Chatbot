"""
Hugging Face CrossEncoder Model.

Implementation of BaseCrossEncoderModel using
Sentence Transformers.
"""

from sentence_transformers import CrossEncoder

from app.core.config import settings
from app.core.logging import get_logger

from .base import BaseCrossEncoderModel


logger = get_logger(__name__)


class HuggingFaceCrossEncoderModel(BaseCrossEncoderModel):
    """
    Hugging Face implementation of the CrossEncoder.
    """

    def __init__(self) -> None:

        logger.info(
            "Loading CrossEncoder model: %s",
            settings.RERANKER_MODEL_NAME,
        )

        self._model = CrossEncoder(
            settings.RERANKER_MODEL_NAME,
        )

        logger.info(
            "CrossEncoder loaded successfully."
        )

    @property
    def model_name(self) -> str:
        """
        Return model name.
        """

        return settings.RERANKER_MODEL_NAME

    def predict(
        self,
        query: str,
        documents: list[str],
    ) -> list[float]:
        """
        Predict semantic relevance scores.
        """

        logger.info("Computing reranking scores for %d documents.",len(documents),)

        pairs = [

            (query, document)

            for document in documents

        ]

        scores = self._model.predict(
            pairs,
        )

        logger.info(
            "Successfully computed reranking scores."
        )

        return scores.tolist()