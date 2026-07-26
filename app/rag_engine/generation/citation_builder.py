"""
Citation Builder.

Builds citations from retrieved document chunks.
"""

from app.core.logging import get_logger

from app.rag_engine.retrieval.schemas.retrieved_chunk import (
    RetrievedChunk,
)

from .schemas.citation import Citation


logger = get_logger(__name__)


class CitationBuilder:
    """
    Builds citations for the generated answer.
    """

    #################
    # Public Methods
    #################

    def build(
        self,
        retrieved_chunks: list[RetrievedChunk],
    ) -> list[Citation]:
        """
        Build citations from retrieved chunks.

        Parameters
        ----------
        retrieved_chunks : list[RetrievedChunk]

        Returns
        -------
        list[Citation]
        """

        logger.info(
            "Building citations from %d retrieved chunk(s).",
            len(retrieved_chunks),
        )

        citations = [

            Citation(

                document_id=chunk.document_id,

                chunk_id=chunk.chunk_id,

                page_number=chunk.page_number,

                score=chunk.score,

            )

            for chunk in retrieved_chunks

        ]

        logger.info(
            "Successfully built %d citation(s).",
            len(citations),
        )

        return citations