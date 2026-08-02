from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.message import MessageCreate



def create_message(
    db: Session,
    user_id: int,
    data: MessageCreate,
) -> Message:

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == data.conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if conversation is None:
        raise ValueError("Conversation not found.")

    # Prevent duplicate webhook processing.
    if data.external_id:
        existing = (
            db.query(Message)
            .filter(
                Message.user_id == user_id,
                Message.platform == data.platform,
                Message.external_id == data.external_id,
            )
            .first()
        )

        if existing:
            return existing

    message = Message(
        user_id=user_id,
        conversation_id=data.conversation_id,
        platform=data.platform,
        external_id=data.external_id,
        direction=data.direction,
        sender_name=data.sender_name,
        sender_identifier=data.sender_identifier,
        recipient_identifier=data.recipient_identifier,
        content=data.content,
        message_type=data.message_type,
        is_read=data.is_read,
        is_important=data.is_important,
    )

    db.add(message)

    conversation.last_message_at = datetime.utcnow()

    db.commit()
    db.refresh(message)

    return message


def get_messages(
    db: Session,
    user_id: int,
    conversation_id: int,
) -> list[Message]:

    return (
        db.query(Message)
        .filter(
            Message.user_id == user_id,
            Message.conversation_id == conversation_id,
        )
        .order_by(Message.received_at.asc())
        .all()
    )