from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.reminder import Reminder
from app.models.task import Task
from app.schemas.reminder import ReminderCreate


def create_appointment_reminder(
    db: Session,
    user_id: int,
    appointment: Appointment,
    data: ReminderCreate,
) -> Reminder:

    reminder = Reminder(
        user_id=user_id,
        appointment_id=appointment.id,
        title=data.title,
        remind_at=data.remind_at,
        notification_channel=data.notification_channel,
        status="pending",
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


def create_task_reminder(
    db: Session,
    user_id: int,
    task: Task,
    data: ReminderCreate,
) -> Reminder:

    reminder = Reminder(
        user_id=user_id,
        task_id=task.id,
        title=data.title,
        remind_at=data.remind_at,
        notification_channel=data.notification_channel,
        status="pending",
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


def get_user_reminders(
    db: Session,
    user_id: int,
) -> list[Reminder]:

    return (
        db.query(Reminder)
        .filter(Reminder.user_id == user_id)
        .order_by(Reminder.remind_at.asc())
        .all()
    )