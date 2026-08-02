from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ContactCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255,
    )

    email: str | None = None

    phone: str | None = None

    notes: str | None = None


class ContactUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    email: str | None = None

    phone: str | None = None

    notes: str | None = None


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str | None
    phone: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )