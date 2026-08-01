from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high|urgent)$",
    )

    due_at: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    status: str | None = Field(
        default=None,
        pattern="^(pending|in_progress|completed|cancelled)$",
    )

    priority: str | None = Field(
        default=None,
        pattern="^(low|medium|high|urgent)$",
    )

    due_at: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    source: str
    due_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )