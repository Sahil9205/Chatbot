"""
Hugging Face Generator.

Concrete implementation of BaseGenerator using
Transformers text-generation pipeline.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from app.core.config import settings
from app.core.logging import get_logger

from .base import BaseGenerator
from .schemas.answer import Answer
from .schemas.finish_reason import FinishReason


logger = get_logger(__name__)


class HuggingFaceGenerator(BaseGenerator):
    """
    Hugging Face implementation of the answer generator.
    """

    def __init__(self) -> None:
        """
        Load tokenizer and model.
        """

        logger.info(
            "Loading generation model: %s",
            settings.LLM_MODEL_NAME,
        )

        self._tokenizer = AutoTokenizer.from_pretrained(
            settings.LLM_MODEL_NAME,
            token=settings.HUGGINGFACE_API_KEY or None,
        )

        self._model = AutoModelForCausalLM.from_pretrained(
            settings.LLM_MODEL_NAME,
            token=settings.HUGGINGFACE_API_KEY or None,
        )

        self._pipeline = pipeline(
            "text-generation",
            model=self._model,
            tokenizer=self._tokenizer,
        )

        logger.info("Generation model loaded successfully.")

    @property
    def model_name(self) -> str:
        """
        Return model name.
        """
        return settings.LLM_MODEL_NAME

    def generate(
        self,
        prompt: str,
    ) -> Answer:
        """
        Generate an answer from the given prompt.

        Parameters
        ----------
        prompt : str

        Returns
        -------
        Answer
        """

        logger.info("Generating answer using Hugging Face model.")

        try:
            outputs = self._pipeline(
                prompt,
                max_new_tokens=settings.MAX_NEW_TOKENS,
                temperature=settings.TEMPERATURE,
                do_sample=settings.TEMPERATURE > 0,
                return_full_text=False,
                pad_token_id=self._tokenizer.eos_token_id,
            )

            generated_text = ""

            if outputs and "generated_text" in outputs[0]:
                generated_text = outputs[0]["generated_text"].strip()

            if not generated_text:
                generated_text = (
                    "I couldn't find sufficient information "
                    "in the provided documents."
                )

            logger.info("Answer generated successfully.")

            return Answer(
                text=generated_text,
                confidence=1.0,
                finish_reason=FinishReason.STOP,
            )

        except Exception as exc:
            logger.exception("Failed to generate answer.")
            raise RuntimeError("Hugging Face generation failed.") from exc