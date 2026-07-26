"""
Abstract interface for answer generation models.
"""

from abc import ABC, abstractmethod

from app.rag_engine.generation.schemas.answer import Answer


class BaseGenerator(ABC):
    """
    Base interface for all answer generation models.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Return the underlying model name.
        """
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> Answer:
        """
        Generate an answer from the supplied prompt.

        Parameters
        ----------
        prompt : str
            Fully constructed prompt.

        Returns
        -------
        Answer
        """
        pass