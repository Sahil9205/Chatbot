"""
LiteLLM Provider
================

This module implements the BaseLLM interface using LiteLLM.

The purpose of this class is to hide all LiteLLM-specific
implementation details from the rest of the application.

Only this file should communicate directly with LiteLLM.
"""

from litellm import acompletion

from app.ai.llm.base import BaseLLM
from app.core import settings


class LiteLLMProvider(BaseLLM):
    """
    LiteLLM implementation of the BaseLLM interface.
    """

    def __init__(self) -> None:
        self.model = settings.DEFAULT_LLM_MODEL

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> str:
        """
        Generate a response from the configured LLM.
        """

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = await acompletion(
            model=self.model,
            messages=messages,
        )

        return response.choices[0].message.content

    async def stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ):
        """
        Streaming support.

        This will be implemented later.
        """

        raise NotImplementedError(
            "Streaming is not implemented yet."
        )