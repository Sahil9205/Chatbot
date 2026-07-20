"""
BM25 Keyword Index
"""

from typing import List

from rank_bm25 import BM25Okapi

from app.core.logging import get_logger

from app.rag_engine.ingestion.chunking.chunk_schema import Chunk
from app.rag_engine.retrieval.schemas.retrieved_chunk import RetrievedChunk

from .base import BaseKeywordIndex
from .tokenizer import Tokenizer


logger = get_logger(__name__)


class BM25Index(BaseKeywordIndex):
    """
    BM25 keyword retrieval implementation.
    """

    def __init__(self):

        self.bm25 = None

        self.documents: List[Chunk] = []

        self.corpus: List[List[str]] = []

    ####################################################################
    # Build Index
    ####################################################################

    def build(self,chunks: List[Chunk],) -> None:
        """
        Build BM25 index from chunks.
        """

        logger.info("Building BM25 index...")

        self.documents = chunks

        self.corpus = [
            Tokenizer.tokenize(chunk.text)
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(self.corpus)

        logger.info("Indexed %d chunks.",len(chunks),)

    ####################################################################
    # Search
    ####################################################################

    def search(self,query: str,top_k: int = 5, ) -> List[RetrievedChunk]:
        """
        Perform keyword search.
        """

        if self.bm25 is None:

            raise RuntimeError("BM25 index has not been built.")

        query_tokens = Tokenizer.tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked = sorted(

            enumerate(scores),

            key=lambda item: item[1],

            reverse=True,
        )

        retrieved_chunks = []

        for index, score in ranked[:top_k]:

            chunk = self.documents[index]

            retrieved_chunks.append(

                RetrievedChunk(

                    chunk_id=chunk.chunk_id,

                    document_id=chunk.document_id,

                    chunk_index=chunk.chunk_index,

                    text=chunk.text,

                    metadata=chunk.metadata,

                    score=float(score),
                )
            )

        return retrieved_chunks