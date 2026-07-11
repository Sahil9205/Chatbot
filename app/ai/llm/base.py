from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Abstract Base Class for all LLM providers."""

    @abstractmethod
    def generate(self,prompt: str,system_prompt: str | None = None,) -> str:
        """
        Generate a response from the language model.

        Parameters
        ----------
        prompt : str
            User prompt.

        system_prompt : str | None
            Optional system prompt.

        Returns
        -------
        str
            Generated response.
        """
        pass

    @abstractmethod
    def stream(self,prompt: str,system_prompt: str | None = None,):
        """
        Stream the generated response.

        Returns
        -------
        Iterator[str]
            Stream of generated tokens.
        """
        pass


    """
Base LLM Interface
==================

This module defines the abstract interface that every LLM provider
must implement.

Why?

The rest of the application (LangGraph, Conversation Engine,
RAG, etc.) should never depend on a specific LLM provider.

Instead, they depend on this interface.

Benefits
--------
- Provider independent
- Easy to replace models
- Easy to test
- Clean architecture
"""
