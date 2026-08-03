from datetime import datetime

from google import genai

from app.ai.base import AIProvider
from app.core.config import settings
from app.schemas.ai_message import AIMessageAnalysis

from app.prompts.message_analysis import MESSAGE_ANALYSIS_SYSTEM_PROMPT


class GeminiProvider(AIProvider):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def analyze_message(
        self,
        message: str,
    ) -> AIMessageAnalysis:

        current_datetime = datetime.now().isoformat()

        prompt = f"""
        {MESSAGE_ANALYSIS_SYSTEM_PROMPT}

        Current date and time:
        {current_datetime}

        Use this date/time as the reference when resolving relative
        expressions such as "today", "tomorrow", "next Monday",
        or "in two hours".

        Message to analyze:
        {message}
        """

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": AIMessageAnalysis.model_json_schema(),
            },
        )

        return AIMessageAnalysis.model_validate_json(
            response.text
        )