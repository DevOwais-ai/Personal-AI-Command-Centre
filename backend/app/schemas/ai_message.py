from datetime import datetime

from pydantic import BaseModel, Field


class ReminderActionData(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    remind_at: datetime

    notification_channel: str = Field(
        default="dashboard",
        pattern="^(dashboard|email|telegram|whatsapp)$",
    )


class TaskActionData(BaseModel):
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


class AppointmentActionData(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    start_at: datetime

    end_at: datetime

    location: str | None = None

    contact_id: int | None = None


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

    action_data: (
        ReminderActionData
        | TaskActionData
        | AppointmentActionData
        | None
    ) = None


class AIMessageAnalysisResponse(BaseModel):
    message_id: int
    ai_summary: str | None
    ai_category: str | None
    ai_priority: str | None
    ai_intent: str | None
    ai_action_required: bool
    ai_processed: bool