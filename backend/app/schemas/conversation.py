from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    platform: str
    external_id: str | None = None
    title: str | None = None
    contact_id: int | None = None


class ConversationResponse(BaseModel):
    id: int
    platform: str
    external_id: str | None
    title: str | None
    status: str
    contact_id: int | None
    last_message_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )