"""
Qdrant Vector Store Implementation.

Responsible for storing and retrieving embeddings
from the Qdrant vector database.
"""

from typing import List

from qdrant_client import QdrantClient
from qdrant_client.models import (ScoredPoint, VectorParams,PointStruct,Filter, Distance,ScoredPoint)

from app.core.config import settings
from app.core.constants import DISTANCE_MAPPING
from app.core.exceptions import (ConfigurationError)

from app.core.logging import get_logger

from .base import BaseVectorStore
from ..embeddings.embedding_schema import EmbeddedChunk


logger = get_logger(__name__)


class QdrantStore(BaseVectorStore):

    """
    Qdrant implementation of BaseVectorStore.
    """

    def __init__(self,embedding_dimension: int,):

        self.client = QdrantClient(

            url=settings.QDRANT_URL,

            api_key=settings.QDRANT_API_KEY,
        )

        self.collection_name = (
            settings.QDRANT_COLLECTION_NAME
        )

        self.embedding_dimension = embedding_dimension

        self.distance = self._load_distance_metric()

        self.create_collection()

    ####################################################################
    # Private Methods
    ####################################################################

    def _load_distance_metric(self) -> Distance:
        """
        Load distance metric from configuration.
        """

        try:

            return DISTANCE_MAPPING[
                settings.QDRANT_DISTANCE_METRIC.upper()
            ]

        except KeyError as e:

            raise ConfigurationError(

                f"Unsupported distance metric: "
                f"{settings.QDRANT_DISTANCE_METRIC}"

            ) from e

    ####################################################################
    # Collection
    ####################################################################

    def collection_exists(self) -> bool:

        collections = self.client.get_collections()

        return any(

            collection.name == self.collection_name

            for collection in collections.collections
        )

    def create_collection(self) -> None:

        if self.collection_exists():

            logger.info("Collection '%s' already exists.",self.collection_name,)

            return

        logger.info("Creating collection '%s'.",self.collection_name,)

        self.client.create_collection(

            collection_name=self.collection_name,

            vectors_config=VectorParams(

                size=self.embedding_dimension,

                distance=self.distance,
            ),
        )

    ####################################################################
    # Insert
    ####################################################################

    def add(self,chunks: List[EmbeddedChunk],) -> None:

        points = []

        for chunk in chunks:

            point = PointStruct(

                id=chunk.chunk_id,

                vector=chunk.embedding,

                payload={

                    "document_id": chunk.document_id,

                    "chunk_index": chunk.chunk_index,

                    "text": chunk.text,

                    "metadata": chunk.metadata,
                },
            )

            points.append(point)

        self.client.upsert(

            collection_name=self.collection_name,

            points=points,
        )

        logger.info("%d vectors inserted.",len(points),)

    ####################################################################
    # Search
    ####################################################################

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        query_filter: Filter | None = None,
        ) -> list[ScoredPoint]:  
        """
        Search for similar vectors in the Qdrant collection.

        Parameters
        ----------
        query_vector : list[float]
            Query embedding.

        top_k : int
            Number of nearest neighbours to retrieve.

        query_filter : Filter | None
            Optional metadata filter.

        Returns
        -------
        list[ScoredPoint]
        """

        logger.info("Searching collection '%s'.",self.collection_name,)

        try:

            results = self.client.search(

                collection_name=self.collection_name,

                query_vector=query_vector,

                query_filter=query_filter,

                limit=top_k,
            )

            logger.info("Retrieved %d result(s).",len(results),)

            return results

        except Exception:

            logger.exception("Failed to search Qdrant collection '%s'.",self.collection_name,)

            raise

    ####################################################################
    # Delete
    ####################################################################

    def delete(self,ids: list[str],) -> None:

        self.client.delete(

            collection_name=self.collection_name,

            points_selector=ids,
        )

        logger.info("%d vectors deleted.",len(ids),)