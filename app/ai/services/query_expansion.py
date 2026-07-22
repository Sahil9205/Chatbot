"""
Query Expansion Service.

This module generates multiple search queries from a user's query
to improve hybrid document retrieval.
"""

from __future__ import annotations

from app.ai.llm.llm import get_llm
from app.ai.prompts.query_expansion import (QUERY_EXPANSION_SYSTEM_PROMPT,)
from app.ai.schemas.expanded_query import ExpandedQuery

from app.core.exceptions import LLMError
from app.core.logging import get_logger

logger = get_logger(__name__)


class QueryExpansion:
    """
    Service responsible for expanding user queries into
    multiple semantically similar search queries.
    """

    def expand(self,query: str,) -> ExpandedQuery:
        """
        Expand a user query into multiple search queries.

        Parameters
        ----------
        query : str
            Original user query.

        Returns
        -------
        ExpandedQuery
            Validated expanded queries.

        Raises
        ------
        ValueError
            If the query is empty.

        LLMError
            If query expansion fails.
        """

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        logger.info("Expanding user query.")

        llm = get_llm()

        prompt = QUERY_EXPANSION_SYSTEM_PROMPT.format(
            query=query,
        )

        try:
            response = llm.invoke(prompt)

            expanded_query = ExpandedQuery.model_validate_json(
                response.content
            )

            logger.info(
                "Successfully expanded user query into %d queries.",
                len(expanded_query.queries),
            )

            return expanded_query

        except Exception as exc:

            logger.exception("Failed to expand user query.")

            raise LLMError("Query expansion failed.") from exc