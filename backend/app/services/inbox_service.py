from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.message import Message


def get_inbox_messages(
    db: Session,
    user_id: int,
    platform: str | None = None,
    unread_only: bool = False,
    important_only: bool = False,
    search: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Message]:

    query = (
        db.query(Message)
        .filter(Message.user_id == user_id)
    )

    if platform:
        query = query.filter(
            Message.platform == platform
        )

    if unread_only:
        query = query.filter(
            Message.is_read.is_(False)
        )

    if important_only:
        query = query.filter(
            Message.is_important.is_(True)
        )

    if search:
        query = query.filter(
            Message.content.ilike(
                f"%{search}%"
            )
        )

    return (
        query
        .order_by(Message.received_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_inbox_stats(
    db: Session,
    user_id: int,
) -> dict:

    total = (
        db.query(func.count(Message.id))
        .filter(Message.user_id == user_id)
        .scalar()
    )

    unread = (
        db.query(func.count(Message.id))
        .filter(
            Message.user_id == user_id,
            Message.is_read.is_(False),
        )
        .scalar()
    )

    important = (
        db.query(func.count(Message.id))
        .filter(
            Message.user_id == user_id,
            Message.is_important.is_(True),
        )
        .scalar()
    )

    unread_important = (
        db.query(func.count(Message.id))
        .filter(
            Message.user_id == user_id,
            Message.is_read.is_(False),
            Message.is_important.is_(True),
        )
        .scalar()
    )

    return {
        "total_messages": total or 0,
        "unread_messages": unread or 0,
        "important_messages": important or 0,
        "unread_important_messages": unread_important or 0,
    }


def get_message(
    db: Session,
    user_id: int,
    message_id: int,
) -> Message | None:

    return (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.user_id == user_id,
        )
        .first()
    )


def mark_message_read(
    db: Session,
    message: Message,
) -> Message:

    message.is_read = True

    db.commit()
    db.refresh(message)

    return message


def mark_message_unread(
    db: Session,
    message: Message,
) -> Message:

    message.is_read = False

    db.commit()
    db.refresh(message)

    return message


def mark_message_important(
    db: Session,
    message: Message,
) -> Message:

    message.is_important = True

    db.commit()
    db.refresh(message)

    return message


def mark_message_unimportant(
    db: Session,
    message: Message,
) -> Message:

    message.is_important = False

    db.commit()
    db.refresh(message)

    return message  