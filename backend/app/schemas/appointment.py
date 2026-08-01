from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    start_at: datetime

    end_at: datetime

    location: str | None = Field(
        default=None,
        max_length=500,
    )

    contact_id: int | None = None


class AppointmentUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    start_at: datetime | None = None

    end_at: datetime | None = None

    location: str | None = Field(
        default=None,
        max_length=500,
    )

    contact_id: int | None = None

    status: str | None = Field(
        default=None,
        pattern="^(scheduled|completed|cancelled)$",
    )


class AppointmentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    start_at: datetime
    end_at: datetime
    location: str | None
    status: str
    calendar_event_id: str | None
    source: str
    contact_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )