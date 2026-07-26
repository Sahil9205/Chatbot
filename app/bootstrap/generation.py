"""
Bootstrap Generation Pipeline.

Creates and wires together all generation components.
"""

from app.rag_engine.generation.answer_generator import (
    AnswerGenerator,
)
from app.rag_engine.generation.citation_builder import (
    CitationBuilder,
)
from app.rag_engine.generation.generation_pipeline import (
    GenerationPipeline,
)
from app.rag_engine.generation.hallucination.hallucination_guard import (
    HallucinationGuard,
)
from app.rag_engine.generation.huggingface_generator import (
    HuggingFaceGenerator,
)
from app.rag_engine.generation.prompt_builder import (
    PromptBuilder,
)
from app.rag_engine.generation.response_validator import (
    ResponseValidator,
)


def build_generation_pipeline() -> GenerationPipeline:
    """
    Build the complete generation pipeline.
    """

    ###############################################################
    # Prompt Builder
    ###############################################################

    prompt_builder = PromptBuilder()

    ###############################################################
    # Generator
    ###############################################################

    generator = HuggingFaceGenerator()

    ###############################################################
    # Answer Generator
    ###############################################################

    answer_generator = AnswerGenerator(
        generator=generator,
        prompt_builder=prompt_builder,
    )

    ###############################################################
    # Citation Builder
    ###############################################################

    citation_builder = CitationBuilder()

    ###############################################################
    # Hallucination Guard
    ###############################################################

    hallucination_guard = HallucinationGuard()

    ###############################################################
    # Response Validator
    ###############################################################

    response_validator = ResponseValidator()

    ###############################################################
    # Generation Pipeline
    ###############################################################

    return GenerationPipeline(
        answer_generator=answer_generator,
        citation_builder=citation_builder,
        hallucination_guard=hallucination_guard,
        response_validator=response_validator,
    )