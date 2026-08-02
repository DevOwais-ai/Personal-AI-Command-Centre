from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageCreate(BaseModel):
    conversation_id: int

    platform: str

    external_id: str | None = None

    direction: str = Field(
        pattern="^(incoming|outgoing)$",
    )

    sender_name: str | None = None

    sender_identifier: str | None = None

    recipient_identifier: str | None = None

    content: str

    message_type: str = "text"

    is_read: bool = False

    is_important: bool = False


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    platform: str
    external_id: str | None
    direction: str
    sender_name: str | None
    sender_identifier: str | None
    recipient_identifier: str | None
    content: str
    message_type: str
    is_read: bool
    is_important: bool
    ai_summary: str | None
    ai_category: str | None
    ai_priority: str | None
    ai_intent: str | None
    ai_action_required: bool
    ai_processed: bool
    ai_status: str
    received_at: datetime
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )