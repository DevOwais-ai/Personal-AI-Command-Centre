from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReminderCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    remind_at: datetime

    notification_channel: str = Field(
        default="dashboard",
        pattern="^(dashboard|email|telegram|whatsapp)$",
    )


class ReminderResponse(BaseModel):
    id: int
    title: str
    remind_at: datetime
    notification_channel: str
    status: str
    sent_at: datetime | None
    task_id: int | None
    appointment_id: int | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )