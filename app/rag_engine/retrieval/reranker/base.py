"""
Abstract CrossEncoder Interface.
"""

from abc import ABC, abstractmethod


class BaseCrossEncoderModel(ABC):
    """
    Base interface for CrossEncoder models.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Return model name.
        """
        pass

    @abstractmethod
    def predict(
        self,query: str,documents: list[str],) -> list[float]:
        """
        Compute semantic relevance scores.

        Parameters
        ----------
        query : str

        documents : list[str]

        Returns
        -------
        list[float]
        """
        pass