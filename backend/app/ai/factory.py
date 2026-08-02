from app.ai.base import AIProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.openai_provider import OpenAIProvider
from app.core.config import settings


def get_ai_provider() -> AIProvider:
    provider = settings.AI_PROVIDER.lower()

    if provider == "gemini":
        return GeminiProvider()

    if provider == "openai":
        return OpenAIProvider()

    raise ValueError(
        f"Unsupported AI provider: {settings.AI_PROVIDER}"
    )