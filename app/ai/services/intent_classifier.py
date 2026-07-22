"""
Intent classification service.
"""

from __future__ import annotations

import json

from app.ai.llm.base import BaseLLM
from app.ai.prompts.intent_classifier import (
    INTENT_CLASSIFIER_SYSTEM_PROMPT,
)
from app.ai.schemas.intent import IntentClassification

from app.core.exceptions import IntentClassificationError
from app.core.logging import get_logger

logger = get_logger(__name__)


class IntentClassifier:
    """
    Classifies the user's query into a predefined intent.
    """

    def __init__(self, llm: BaseLLM) -> None:
        """
        Initialize the intent classifier.

        Parameters
        ----------
        llm : BaseLLM
            LLM implementation used for intent classification.
        """
        self.llm = llm

    def classify(
        self,
        query: str,
    ) -> IntentClassification:
        """
        Classify the user query.

        Parameters
        ----------
        query : str
            User input.

        Returns
        -------
        IntentClassification

        Raises
        ------
        IntentClassificationError
            If classification fails.
        """

        if not query.strip():
            raise IntentClassificationError(
                "Query cannot be empty."
            )

        logger.info("Classifying query intent.")

        prompt = INTENT_CLASSIFIER_SYSTEM_PROMPT.format(
            query=query,
        )

        try:
            response = self.llm.invoke(prompt)
        except Exception as exc:
            logger.exception(
                "LLM invocation failed during intent classification."
            )
            raise IntentClassificationError(
                "Failed to classify query intent."
            ) from exc

        try:
            result = json.loads(response)
        except json.JSONDecodeError as exc:
            logger.exception(
                "LLM returned invalid JSON."
            )
            raise IntentClassificationError(
                "Invalid JSON returned by LLM."
            ) from exc

        try:
            classification = IntentClassification(**result)
        except Exception as exc:
            logger.exception(
                "Invalid intent classification schema."
            )
            raise IntentClassificationError(
                "Failed to validate intent classification."
            ) from exc

        logger.info(
            "Intent classified successfully: %s",
            classification.intent,
        )

        return classification