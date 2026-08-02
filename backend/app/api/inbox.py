from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.inbox import (
    InboxMessageResponse,
    InboxStatsResponse,
)
from app.services.inbox_service import (
    get_inbox_messages,
    get_inbox_stats,
    get_message,
    mark_message_important,
    mark_message_read,
    mark_message_unimportant,
    mark_message_unread,
)

from app.schemas.ai_message import (
    AIMessageAnalysis,
    AIMessageAnalysisResponse,
)
from app.services.ai_message_service import (
    analyze_and_save_message,
    save_ai_analysis,
)

router = APIRouter(
    prefix="/inbox",
    tags=["Unified Inbox"],
)

@router.get(
    "/messages",
    response_model=list[InboxMessageResponse],
)
def inbox_messages(
    platform: str | None = None,
    unread_only: bool = False,
    important_only: bool = False,
    search: str | None = None,
    priority: str | None = None,
    category: str | None = None,
    intent: str | None = None,
    action_required: bool | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_inbox_messages(
        db=db,
        user_id=current_user.id,
        platform=platform,
        unread_only=unread_only,
        important_only=important_only,
        search=search,
        priority=priority,
        category=category,
        intent=intent,
        action_required=action_required,
        limit=min(limit, 100),
        offset=offset,
    )

@router.get(
    "/stats",
    response_model=InboxStatsResponse,
)
def inbox_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_inbox_stats(
        db=db,
        user_id=current_user.id,
    )

@router.patch(
    "/messages/{message_id}/read",
    response_model=InboxMessageResponse,
)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = get_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found.",
        )

    return mark_message_read(
        db=db,
        message=message,
    )

@router.patch(
    "/messages/{message_id}/unread",
    response_model=InboxMessageResponse,
)
def unread_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = get_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found.",
        )

    return mark_message_unread(
        db=db,
        message=message,
    )

@router.patch(
    "/messages/{message_id}/important",
    response_model=InboxMessageResponse,
)
def important_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = get_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found.",
        )

    return mark_message_important(
        db=db,
        message=message,
    )

@router.patch(
    "/messages/{message_id}/unimportant",
    response_model=InboxMessageResponse,
)
def unimportant_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = get_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found.",
        )

    return mark_message_unimportant(
        db=db,
        message=message,
    )


@router.patch(
    "/messages/{message_id}/analysis",
    response_model=InboxMessageResponse,
)
def analyze_message(
    message_id: int,
    analysis: AIMessageAnalysis,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = get_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found.",
        )

    return save_ai_analysis(
        db=db,
        message=message,
        analysis=analysis,
    )

@router.post(
    "/messages/{message_id}/analyze",
    response_model=AIMessageAnalysisResponse,
)
def analyze_message_with_ai(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = get_message(
        db=db,
        user_id=current_user.id,
        message_id=message_id,
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found.",
        )

    message = analyze_and_save_message(
    db=db,
    message=message,
    )

    return AIMessageAnalysisResponse(
        message_id=message.id,
        ai_summary=message.ai_summary,
        ai_category=message.ai_category,
        ai_priority=message.ai_priority,
        ai_intent=message.ai_intent,
        ai_action_required=message.ai_action_required,
        ai_processed=message.ai_processed,
    )