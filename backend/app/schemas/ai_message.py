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