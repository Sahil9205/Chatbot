"""
Answer Generator.

Generates an answer from a fully constructed prompt.
"""

from app.core.logging import get_logger

from .base import BaseGenerator
from .prompt_builder import PromptBuilder
from .schemas.answer import Answer
from .schemas.generation_request import GenerationRequest

logger = get_logger(__name__)


class AnswerGenerator:
    """
    Coordinates prompt construction and answer generation.
    """

    def __init__(
        self,
        generator: BaseGenerator,
        prompt_builder: PromptBuilder,
    ) -> None:
        """
        Parameters
        ----------
        generator : BaseGenerator
            Underlying language model.

        prompt_builder : PromptBuilder
            Builds the prompt for the model.
        """

        self.generator = generator

        self.prompt_builder = prompt_builder

    ####################################################################
    # Public Methods
    ####################################################################

    def generate(
        self,
        request: GenerationRequest,
    ) -> Answer:
        """
        Generate an answer.

        Parameters
        ----------
        request : GenerationRequest

        Returns
        -------
        Answer
        """

        logger.info("Generating answer using %s.", self.generator.model_name)

        try:

            prompt = self.prompt_builder.build(
                request,
            )

            answer = self.generator.generate(
                prompt,
            )

            logger.info("Answer generated successfully.")

            return answer

        except Exception:

            logger.exception("Answer generation failed.")

            raise