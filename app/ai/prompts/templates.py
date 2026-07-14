"""
Prompt Templates

This module contains reusable prompt templates used by the chatbot.

Prompt templates combine:

- System Prompt
- Retrieved Context
- Conversation History
- User Question

into a final prompt sent to the LLM.
"""

from langchain_core.prompts import ChatPromptTemplate

from app.ai.prompts.system import COMPANY_ASSISTANT_SYSTEM_PROMPT


CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            COMPANY_ASSISTANT_SYSTEM_PROMPT,
        ),
        (
            "system",
            """
Retrieved Context:

{context}
""",
        ),
        (
            "system",
            """
Conversation History:

{chat_history}
""",
        ),
        (
            "human",
            "{question}",
        ),
    ]
)