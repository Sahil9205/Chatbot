"""
Response Validator.

Validates the final generated response before it is
returned to the user.
"""

from app.core.logging import get_logger

from .schemas.generation_response import GenerationResponse

logger = get_logger(__name__)


class ResponseValidator:
    """
    Validates the generated response.
    """

    ####################################################################
    # Public Methods
    ####################################################################

    def validate(
        self,
        response: GenerationResponse,
    ) -> GenerationResponse:
        """
        Validate a generated response.

        Parameters
        ----------
        response : GenerationResponse

        Returns
        -------
        GenerationResponse
        """

        logger.info("Validating generation response.")

        if not response.answer.text.strip():

            raise ValueError(
                "Generated answer cannot be empty."
            )

        if not response.has_sufficient_context:

            raise ValueError("Insufficient supporting context.")

        if not response.citations:

            raise ValueError(
                "No citations found."
            )

        logger.info(
            "Generation response validated successfully."
        )

        return response