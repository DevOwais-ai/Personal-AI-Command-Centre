from sqlalchemy.orm import Session

from app.models.message import Message


SUPPORTED_ACTIONS = {
    "reminder",
    "task",
    "appointment",
}


def dispatch_action(
    db: Session,
    message: Message,
) -> str | None:
    """
    Determine which action should handle an AI-analyzed message.

    This step only routes the intent.
    Actual action execution will be implemented separately.
    """

    if not message.ai_processed:
        return None

    if not message.ai_action_required:
        return None

    intent = (message.ai_intent or "").strip().lower()

    if intent not in SUPPORTED_ACTIONS:
        return None

    return intent