"""
Application Constants
"""

from qdrant_client.models import Distance


DISTANCE_MAPPING = {
    "COSINE": Distance.COSINE,
    "DOT": Distance.DOT,
    "EUCLID": Distance.EUCLID,
    "MANHATTAN": Distance.MANHATTAN,
}