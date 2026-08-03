from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.ai_message import (
    ReminderActionData,
    TaskActionData,
    AppointmentActionData,
)
from app.schemas.reminder import ReminderCreate
from app.schemas.task import TaskCreate
from app.schemas.appointment import AppointmentCreate
from app.services.reminder_service import create_reminder
from app.services.task_service import create_task
from app.services.appointment_service import create_appointment


def execute_action(
    db: Session,
    message: Message,
    action_type: str,
    action_data,
) -> dict:

    supported_actions = {
        "reminder",
        "task",
        "appointment",
    }

    if action_type not in supported_actions:
        raise ValueError(
            f"Unsupported action type: {action_type}"
        )

    if action_data is None:
        raise ValueError(
            f"Action data is required for '{action_type}'."
        )

    user_id = message.conversation.user_id

    if action_type == "reminder":

        if not isinstance(action_data, ReminderActionData):
            raise ValueError(
                "Invalid action data for reminder."
            )

        reminder_data = ReminderCreate(
            title=action_data.title,
            remind_at=action_data.remind_at,
            notification_channel=action_data.notification_channel,
        )

        reminder = create_reminder(
            db=db,
            user_id=user_id,
            data=reminder_data,
        )

        return {
            "status": "completed",
            "action_type": "reminder",
            "message_id": message.id,
            "reminder_id": reminder.id,
        }

    if action_type == "task":

        if not isinstance(action_data, TaskActionData):
            raise ValueError(
                "Invalid action data for task."
            )

        task_data = TaskCreate(
            title=action_data.title,
            description=action_data.description,
            priority=action_data.priority,
            due_at=action_data.due_at,
        )

        task = create_task(
            db=db,
            user_id=user_id,
            data=task_data,
        )

        return {
            "status": "completed",
            "action_type": "task",
            "message_id": message.id,
            "task_id": task.id,
        }

    if action_type == "appointment":

        if not isinstance(action_data, AppointmentActionData):
            raise ValueError(
                "Invalid action data for appointment."
            )

        appointment_data = AppointmentCreate(
            title=action_data.title,
            description=action_data.description,
            start_at=action_data.start_at,
            end_at=action_data.end_at,
            location=action_data.location,
            contact_id=action_data.contact_id,
        )

        appointment = create_appointment(
            db=db,
            user_id=user_id,
            data=appointment_data,
        )

        return {
            "status": "completed",
            "action_type": "appointment",
            "message_id": message.id,
            "appointment_id": appointment.id,
        }

    raise ValueError(
        f"Unhandled action type: {action_type}"
    )