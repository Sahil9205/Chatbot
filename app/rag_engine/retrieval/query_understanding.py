"""
Query Understanding.

This module orchestrates all query understanding components
to prepare a search query for retrieval.
"""

from app.ai.prompts import intent_classifier
from app.ai.schemas.intent import Intent

from app.ai.services.intent_classifier import IntentClassifier
from app.ai.services.metadata_extractor import MetadataExtractor
from app.ai.services.query_expansion import QueryExpansion
from app.ai.services.query_rewriter import QueryRewriter

from app.core.logging import get_logger

from .schemas.query import SearchQuery

logger = get_logger(__name__)


class QueryUnderstanding:
    """
    Orchestrates the complete query understanding pipeline.
    """

    def __init__(
    self,
    intent_classifier: IntentClassifier,
    query_rewriter: QueryRewriter,
    query_expansion: QueryExpansion,
    metadata_extractor: MetadataExtractor,
    ) -> None:
        """
        Initialize the query understanding pipeline.

        Parameters
        ----------
        intent_classifier : IntentClassifier

        query_rewriter : QueryRewriter

        query_expansion : QueryExpansion

        metadata_extractor : MetadataExtractor
        """

        self.intent_classifier = intent_classifier
        self.query_rewriter = query_rewriter
        self.query_expansion = query_expansion
        self.metadata_extractor = metadata_extractor


    def process(self,query: str,) -> SearchQuery:
        """
        Process a user query before retrieval.

        Parameters
        ----------
        query : str

        Returns
        -------
        SearchQuery
        """

        logger.info("Starting query understanding pipeline.")

        intent = self.intent_classifier.classify(query)

        logger.info("Detected intent: %s",intent.intent.value,)

        if intent.intent != Intent.DOCUMENT_SEARCH:

            logger.info("Query does not require document retrieval.")

            return SearchQuery(
                original_query=query,
                rewritten_query=query,
            )

        rewritten = self.query_rewriter.rewrite(query)

        expanded = self.query_expansion.expand(rewritten.query,)

        metadata = self.metadata_extractor.extract(rewritten.query,)

        logger.info("Query understanding completed successfully.")

        return SearchQuery(

            original_query=query,

            rewritten_query=rewritten.query,

            expanded_queries=expanded.queries,

            metadata_filters={
                item.field: item.value
                for item in metadata.filters
            },
        )