"""
Reciprocal Rank Fusion (RRF)

Fuses multiple ranked retrieval results into a single
ranking using the Reciprocal Rank Fusion algorithm.
"""

from torch import chunk

from app.core.config import settings
from app.core.logging import get_logger

from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk

from .base import BaseFusionStrategy


logger = get_logger(__name__)


class ReciprocalRankFusion(BaseFusionStrategy):
    """
    Reciprocal Rank Fusion implementation.
    """

    def __init__(
        self,
        rrf_k: int | None = None,
        top_k: int | None = None,) -> None:
        """
        Parameters
        ----------
        rrf_k : int | None
            RRF constant.

        top_k : int | None
            Maximum number of fused results.
        """

        self.rrf_k = rrf_k or settings.RRF_K

        self.top_k = top_k or settings.FINAL_TOP_K

    ####################
    # Public Methods
    ####################

    def fuse(
        self,
        *ranked_lists: list[RetrievedChunk],) -> list[RetrievedChunk]:
        """
        Fuse multiple ranked lists.

        Parameters
        ----------
        ranked_lists : list[RetrievedChunk]

        Returns
        -------
        list[RetrievedChunk]
        """

        logger.info(
            "Running Reciprocal Rank Fusion on %d ranked list(s).",
            len(ranked_lists),
        )

        try:

            fused_scores: dict[str, float] = {}

            chunk_lookup: dict[str, RetrievedChunk] = {}

            for ranked_list in ranked_lists:

                for rank, chunk in enumerate(
                    ranked_list,
                    start=1,
                ):

                    fused_scores.setdefault(
                        chunk.chunk_id,
                        0.0,
                    )

                    fused_scores[chunk.chunk_id] += (

                        1.0 / (self.rrf_k + rank)

                    )

                    if chunk.chunk_id not in chunk_lookup:

                        chunk_lookup[chunk.chunk_id] = chunk

            ranked_chunk_ids = sorted(

                fused_scores,

                key=fused_scores.get,

                reverse=True,
            )

            fused_results: list[RetrievedChunk] = []

            for chunk_id in ranked_chunk_ids[: self.top_k]:

                original = chunk_lookup[chunk_id]

                fused_results.append(

                    RetrievedChunk(

                        chunk_id=original.chunk_id,

                        document_id=original.document_id,

                        chunk_index=original.chunk_index,

                        text=original.text,

                        metadata=original.metadata,

                        score=fused_scores[chunk_id],

                        source="hybrid",
                    )

                )

            logger.info("Fusion completed with %d result(s).",len(fused_results),)

            return fused_results

        except Exception:

            logger.exception(
                "Reciprocal Rank Fusion failed."
            )

            raise