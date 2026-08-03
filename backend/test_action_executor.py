from app.database.session import SessionLocal
from app.models.message import Message
# from app.schemas.ai_message import TaskActionData
from app.schemas.ai_message import AppointmentActionData
from app.services.action_executor import execute_action


db = SessionLocal()

try:
    message = (
        db.query(Message)
        .filter(Message.id == 15)
        .first()
    )

    if message is None:
        raise ValueError("Message 15 not found.")

    action_data = AppointmentActionData(
    title="Test client meeting",
    description="Discuss the client proposal.",
    start_at="2026-08-05T14:00:00",
    end_at="2026-08-05T15:00:00",
    location="Online",
    )

    result = execute_action(
        db=db,
        message=message,
        action_type="appointment",
        action_data=action_data,
    )

    print("Executor result:", result)

finally:
    db.close()