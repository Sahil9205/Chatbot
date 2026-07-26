"""
Prompt Builder.

Constructs the prompt passed to the language model.
"""

from app.core.logging import get_logger

from .schemas.generation_request import GenerationRequest


logger = get_logger(__name__)


class PromptBuilder:
    """
    Builds prompts for the language model.
    """

    DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant.

Answer ONLY using the provided context.

Rules:
1. Never invent information.
2. If the answer is not present in the context, say:
   "I couldn't find sufficient information in the provided documents."
3. Keep the answer concise.
4. Cite information only from the supplied context.
""".strip()

    ####################################################################
    # Public API
    ####################################################################

    def build(
        self,
        request: GenerationRequest,
    ) -> str:
        """
        Build the final prompt.
        """

        logger.info("Building generation prompt.")

        system_prompt = (
            request.system_prompt
            or self.DEFAULT_SYSTEM_PROMPT
        )

        context = self._build_context(request)

        prompt = f"""
{system_prompt}

========================
Context
========================

{context}

========================
Question
========================

{request.query}

========================
Answer
========================
""".strip()

        logger.info("Prompt built successfully.")

        return prompt

    ####################################################################
    # Private Helpers
    ####################################################################

    def _build_context(
        self,
        request: GenerationRequest,
    ) -> str:
        """
        Convert retrieved chunks into context.
        """

        parts = []

        for index, chunk in enumerate(
            request.retrieved_chunks,
            start=1,
        ):

            page = (
                chunk.page_number
                if chunk.page_number is not None
                else "Unknown"
            )

            parts.append(

                f"[Document {index}]\n"
                f"Document ID : {chunk.document_id}\n"
                f"Page        : {page}\n"
                f"Content:\n"
                f"{chunk.text}"
            )

        return "\n\n".join(parts)