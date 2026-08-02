from sqlalchemy.orm import Session

from app.ai.factory import get_ai_provider
from app.models.message import Message
from app.schemas.ai_message import AIMessageAnalysis


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

    return message


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