from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InboxMessageResponse(BaseModel):
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

    received_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class InboxStatsResponse(BaseModel):
    total_messages: int
    unread_messages: int
    important_messages: int
    unread_important_messages: int