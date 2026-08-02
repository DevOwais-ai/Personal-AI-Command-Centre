from datetime import datetime

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate


def create_conversation(
    db: Session,
    user_id: int,
    data: ConversationCreate,
) -> Conversation:

    conversation = Conversation(
        user_id=user_id,
        platform=data.platform,
        external_id=data.external_id,
        title=data.title,
        contact_id=data.contact_id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversations(
    db: Session,
    user_id: int,
) -> list[Conversation]:

    return (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(
            Conversation.last_message_at.desc().nullslast()
        )
        .all()
    )