from sqlalchemy.orm import Session

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
    message.ai_processed = True

    if analysis.priority in {"high", "urgent"}:
        message.is_important = True

    db.commit()
    db.refresh(message)

    return message