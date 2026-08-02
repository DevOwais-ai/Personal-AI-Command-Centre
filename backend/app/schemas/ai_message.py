from pydantic import BaseModel, Field


class AIMessageAnalysis(BaseModel):
    summary: str = Field(
        min_length=1,
        max_length=1000,
    )

    category: str = Field(
        min_length=1,
        max_length=50,
    )

    priority: str = Field(
        pattern="^(low|normal|high|urgent)$",
    )

    intent: str = Field(
        min_length=1,
        max_length=50,
    )

    action_required: bool


class AIMessageAnalysisResponse(BaseModel):
    message_id: int
    ai_summary: str | None
    ai_category: str | None
    ai_priority: str | None
    ai_intent: str | None
    ai_action_required: bool
    ai_processed: bool