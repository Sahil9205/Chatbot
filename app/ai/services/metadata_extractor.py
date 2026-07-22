"""
Metadata Extraction Service.

This module extracts metadata filters from a user's query
to improve filtered document retrieval.
"""

from __future__ import annotations

from app.ai.llm.llm import get_llm
from app.ai.prompts.metadata_extractor import (METADATA_EXTRACTOR_SYSTEM_PROMPT,)
from app.ai.schemas.metadata import MetadataExtraction

from app.core.exceptions import LLMError
from app.core.logging import get_logger

logger = get_logger(__name__)


class MetadataExtractor:
    """
    Service responsible for extracting metadata filters
    from a user's query.
    """

    def extract(self,query: str,) -> MetadataExtraction:
        """
        Extract metadata filters from a user query.

        Parameters
        ----------
        query : str
            Original user query.

        Returns
        -------
        MetadataExtraction
            Validated metadata filters.

        Raises
        ------
        ValueError
            If the query is empty.

        LLMError
            If metadata extraction fails.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        logger.info("Extracting metadata filters.")

        llm = get_llm()

        prompt = METADATA_EXTRACTOR_SYSTEM_PROMPT.format(
            query=query,
        )

        try:
            response = llm.invoke(prompt)

            metadata = MetadataExtraction.model_validate_json(response.content)

            logger.info("Successfully extracted %d metadata filter(s).",len(metadata.filters),)

            return metadata

        except Exception as exc:

            logger.exception("Failed to extract metadata filters.")

            raise LLMError("Metadata extraction failed." ) from exc