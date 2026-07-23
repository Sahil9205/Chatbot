"""
BM25 Keyword Index

Responsible for building and searching a BM25 keyword index.
"""

from rank_bm25 import BM25Okapi

from app.core.logging import get_logger
from app.rag_engine.ingestion.chunking.chunk_schema import Chunk

from .base import BaseKeywordIndex
from .bm25_result import BM25Result
from .tokenizer import Tokenizer


logger = get_logger(__name__)


class BM25Index(BaseKeywordIndex):
    """
    BM25 keyword retrieval implementation.
    """

    def __init__(self) -> None:

        self.bm25: BM25Okapi | None = None

        self.documents: list[Chunk] = []

        self.corpus: list[list[str]] = []

    ####################################################################
    # Build Index
    ####################################################################

    def build(self,chunks: list[Chunk],) -> None:
        """
        Build the BM25 index.

        Parameters
        ----------
        chunks : list[Chunk]
            Document chunks to index.
        """

        logger.info("Building BM25 index...")

        try:

            self.documents = chunks

            self.corpus = [

                Tokenizer.tokenize(chunk.text)

                for chunk in chunks
            ]

            self.bm25 = BM25Okapi(self.corpus)

            logger.info("Successfully indexed %d chunk(s).",len(chunks),)

        except Exception:

            logger.exception("Failed to build BM25 index.")

            raise

    ####################################################################
    # Search
    ####################################################################

    def search(self,query: str,top_k: int = 5,) -> list[BM25Result]:
        """
        Perform keyword search.

        Parameters
        ----------
        query : str

        top_k : int

        Returns
        -------
        list[BM25Result]
        """

        if self.bm25 is None:

            raise RuntimeError(
                "BM25 index has not been built."
            )

        logger.info("Performing BM25 search.")

        try:

            query_tokens = Tokenizer.tokenize(query)

            scores = self.bm25.get_scores(query_tokens)

            ranked_results = sorted(

                enumerate(scores),

                key=lambda item: item[1],

                reverse=True,
            )

            results: list[BM25Result] = []

            for index, score in ranked_results[:top_k]:

                chunk = self.documents[index]

                results.append(

                    BM25Result(

                        chunk_id=chunk.chunk_id,

                        document_id=chunk.document_id,

                        chunk_index=chunk.chunk_index,

                        text=chunk.text,

                        score=float(score),

                        metadata=chunk.metadata,
                    )

                )

            logger.info("BM25 returned %d result(s).",len(results),)

            return results

        except Exception:

            logger.exception("BM25 search failed.")

            raise