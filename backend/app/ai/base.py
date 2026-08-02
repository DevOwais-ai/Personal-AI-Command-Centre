from abc import ABC, abstractmethod

from app.schemas.ai_message import AIMessageAnalysis


class AIProvider(ABC):

    @abstractmethod
    def analyze_message(
        self,
        message: str,
    ) -> AIMessageAnalysis:
        pass