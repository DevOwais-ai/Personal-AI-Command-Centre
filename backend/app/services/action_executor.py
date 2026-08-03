from sqlalchemy.orm import Session

from app.models.message import Message
from app.models.ai_action import AIAction

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

    # Create AIAction execution record
    ai_action = AIAction(
        user_id=user_id,
        message_id=message.id,
        action_type=action_type,
        agent="action_executor",
        input_data=action_data.model_dump(mode="json"),
        status="processing",
        requires_approval=False,
    )

    db.add(ai_action)
    db.commit()
    db.refresh(ai_action)

    try:

        # -------------------------
        # Reminder
        # -------------------------
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

            ai_action.status = "completed"
            ai_action.output_data = {
                "reminder_id": reminder.id,
            }

            db.commit()

            return {
                "status": "completed",
                "action_type": "reminder",
                "message_id": message.id,
                "ai_action_id": ai_action.id,
                "reminder_id": reminder.id,
            }

        # -------------------------
        # Task
        # -------------------------
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

            ai_action.status = "completed"
            ai_action.output_data = {
                "task_id": task.id,
            }

            db.commit()

            return {
                "status": "completed",
                "action_type": "task",
                "message_id": message.id,
                "ai_action_id": ai_action.id,
                "task_id": task.id,
            }

        # -------------------------
        # Appointment
        # -------------------------
        if action_type == "appointment":

            if not isinstance(
                action_data,
                AppointmentActionData,
            ):
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

            ai_action.status = "completed"
            ai_action.output_data = {
                "appointment_id": appointment.id,
            }

            db.commit()

            return {
                "status": "completed",
                "action_type": "appointment",
                "message_id": message.id,
                "ai_action_id": ai_action.id,
                "appointment_id": appointment.id,
            }

        raise ValueError(
            f"Unhandled action type: {action_type}"
        )

    except Exception as exc:

        # Roll back any uncommitted database changes
        db.rollback()

        # Reload the AIAction record after rollback
        ai_action = (
            db.query(AIAction)
            .filter(AIAction.id == ai_action.id)
            .first()
        )

        if ai_action is not None:
            ai_action.status = "failed"
            ai_action.output_data = {
                "error": str(exc),
            }

            db.commit()

        return {
            "status": "failed",
            "action_type": action_type,
            "message_id": message.id,
            "ai_action_id": ai_action.id if ai_action else None,
            "error": str(exc),
        }
