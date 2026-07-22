"""
Query Rewriter Service.

This module rewrites user queries to improve retrieval quality.
"""

from __future__ import annotations

import json

from app.ai.llm.llm import get_llm
from app.ai.prompts.query_rewriter import (
    QUERY_REWRITER_SYSTEM_PROMPT,
)
from app.ai.schemas.rewritten_query import RewrittenQuery

from app.core.exceptions import LLMError
from app.core.logging import get_logger

logger = get_logger(__name__)


class QueryRewriter:
    """
    Service responsible for rewriting user queries.
    """

    def rewrite(
        self,
        query: str,
    ) -> RewrittenQuery:
        """
        Rewrite the user query.

        Parameters
        ----------
        query : str
            Original user query.

        Returns
        -------
        RewrittenQuery

        Raises
        ------
        ValueError
            If the query is empty.

        LLMError
            If rewriting fails.
        """

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        logger.info("Rewriting user query.")

        llm = get_llm()

        prompt = QUERY_REWRITER_SYSTEM_PROMPT.format(
            query=query,
        )

        try:
            response = llm.invoke(prompt)

            rewritten_query = RewrittenQuery.model_validate_json(
                response.content
            )

            logger.info(
                "Successfully rewrote query."
            )

            return rewritten_query

        except Exception as exc:

            logger.exception(
                "Failed to rewrite query."
            )

            raise LLMError(
                "Query rewriting failed."
            ) from exc