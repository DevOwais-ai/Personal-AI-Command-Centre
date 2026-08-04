from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.appointment import Appointment
from app.models.user import User
from app.schemas.reminder import (
    ReminderCreate,
    ReminderResponse,
)
from app.services.reminder_service import (
    create_appointment_reminder,
    get_user_reminders,
)
from datetime import timezone

router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"],
)

@router.post(
    "/appointments/{appointment_id}",
    response_model=ReminderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reminder_for_appointment(
    appointment_id: int,
    data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.user_id == current_user.id,
        )
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    appointment_start = appointment.start_at

    if appointment_start.tzinfo is None:
        appointment_start = appointment_start.replace(
            tzinfo=timezone.utc
        )

    if data.remind_at >= appointment_start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reminder must be before the appointment.",
        )

    return create_appointment_reminder(
        db=db,
        user_id=current_user.id,
        appointment=appointment,
        data=data,
    )

@router.get(
    "",
    response_model=list[ReminderResponse],
)
def list_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_reminders(
        db=db,
        user_id=current_user.id,
    )