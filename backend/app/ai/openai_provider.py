from openai import OpenAI

from app.ai.base import AIProvider
from app.core.config import settings
from app.schemas.ai_message import AIMessageAnalysis


class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def analyze_message(
        self,
        message: str,
    ) -> AIMessageAnalysis:

        response = self.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You analyze incoming personal messages. "
                        "Classify the message and return a concise summary. "
                        "Determine whether the user needs to take action."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text_format=AIMessageAnalysis,
        )

        return response.output_parsed