from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.models.message import Message
from app.schemas.ai_message import (
    AIMessageAnalysis,
    AIMessageAnalysisResponse,
)


def save_ai_analysis(
    db: Session,
    message: Message,
    analysis: AIMessageAnalysis,
) -> Message:

    message.ai_summary = analysis.summary
    message.ai_category = analysis.category
    message.ai_priority = analysis.priority
    message.ai_intent = analysis.intent
    message.ai_action_required = analysis.action_required

    # AI processing completed successfully
    message.ai_processed = True
    message.ai_status = "completed"

    if analysis.priority in {"high", "urgent"}:
        message.is_important = True

    db.commit()
    db.refresh(message)

    return AIMessageAnalysisResponse(
    message_id=message.id,
    ai_summary=message.ai_summary,
    ai_category=message.ai_category,
    ai_priority=message.ai_priority,
    ai_intent=message.ai_intent,
    ai_action_required=message.ai_action_required,
    ai_processed=message.ai_processed,
    )


def analyze_and_save_message(
    db: Session,
    message: Message,
) -> Message:

    # Already successfully analyzed
    if message.ai_processed:
        return message

    if not message.content:
        message.ai_status = "failed"
        db.commit()

        raise ValueError(
            "Cannot analyze a message without content."
        )

    try:
        # Mark as processing before calling AI
        message.ai_status = "processing"
        db.commit()

        provider = get_ai_provider()

        analysis = provider.analyze_message(
            message.content
        )

        return save_ai_analysis(
            db=db,
            message=message,
            analysis=analysis,
        )

    except Exception as exc:
        db.rollback()

        # Reload the message after rollback
        db.refresh(message)

        message.ai_status = "failed"
        message.ai_processed = False

        db.commit()

        print(
            f"AI analysis failed for message "
            f"{message.id}: {exc}"
        )

        return message

def retry_ai_analysis(
    db: Session,
    message: Message,
) -> Message:

    if message.ai_status != "failed":
        raise ValueError(
            "Only failed messages can be retried."
        )

    message.ai_processed = False
    message.ai_status = "pending"

    db.commit()
    db.refresh(message)

    return analyze_and_save_message(
        db=db,
        message=message,
    )

def get_pending_ai_messages(
    db: Session,
    user_id: int,
    limit: int = 10,
) -> list[Message]:
    return (
        db.query(Message)
        .filter(
            Message.user_id == user_id,
            Message.ai_processed.is_(False),
            Message.ai_status == "pending",
        )
        .order_by(Message.created_at.asc())
        .limit(limit)
        .all()
    )

def process_pending_ai_messages(
    db: Session,
    user_id: int,
    limit: int = 10,
) -> int:

    messages = get_pending_ai_messages(
        db=db,
        user_id=user_id,
        limit=limit,
    )

    processed_count = 0

    for message in messages:
        try:
            analyze_and_save_message(
                db=db,
                message=message,
            )

            if message.ai_status == "completed":
                processed_count += 1

        except Exception as exc:
            print(
                f"Failed to process message "
                f"{message.id}: {exc}"
            )

    return processed_count