"""
BM25 Tokenizer.

Converts raw text into normalized tokens suitable
for BM25 keyword indexing.
"""

from __future__ import annotations

import re


class Tokenizer:
    """
    Utility class for BM25 tokenization.
    """

    @staticmethod
    def tokenize(
        text: str,
    ) -> list[str]:
        """
        Convert text into lowercase word tokens.

        Parameters
        ----------
        text : str

        Returns
        -------
        list[str]
        """

        if not text:
            return []

        return re.findall(
            r"\b\w+\b",
            text.lower(),
        )