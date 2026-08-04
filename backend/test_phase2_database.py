from app.database.session import SessionLocal
from app.models.message import Message
from app.models.ai_action import AIAction
from app.models.reminder import Reminder


db = SessionLocal()

try:
    # Use the successful E2E message from Step 24.1
    message_id = 22

    # ---------------------------------------------------------
    # 1. Verify Message
    # ---------------------------------------------------------
    message = (
        db.query(Message)
        .filter(Message.id == message_id)
        .first()
    )

    if message is None:
        raise AssertionError(
            f"Message {message_id} not found."
        )

    print("--- MESSAGE ---")
    print("Message ID:", message.id)
    print("User ID:", message.user_id)
    print("AI status:", message.ai_status)
    print("AI processed:", message.ai_processed)
    print("AI intent:", message.ai_intent)
    print("Action required:", message.ai_action_required)

    assert message.ai_status == "completed"
    assert message.ai_processed is True
    assert message.ai_action_required is True

    # ---------------------------------------------------------
    # 2. Verify AIAction
    # ---------------------------------------------------------
    action = (
        db.query(AIAction)
        .filter(
            AIAction.message_id == message.id
        )
        .first()
    )

    if action is None:
        raise AssertionError(
            "No AIAction found for the message."
        )

    print("\n--- AI ACTION ---")
    print("Action ID:", action.id)
    print("Message ID:", action.message_id)
    print("User ID:", action.user_id)
    print("Action type:", action.action_type)
    print("Agent:", action.agent)
    print("Status:", action.status)
    print("Input data:", action.input_data)
    print("Output data:", action.output_data)

    # Message ownership must match action ownership
    assert action.message_id == message.id
    assert action.user_id == message.user_id

    # The action should have completed
    assert action.status == "completed"

    # This test was specifically for a reminder
    assert action.action_type == "reminder"
    assert action.agent == "action_executor"

    # ---------------------------------------------------------
    # 3. Verify Reminder
    # ---------------------------------------------------------
    if not action.output_data:
        raise AssertionError(
            "AIAction has no output_data."
        )

    reminder_id = action.output_data.get(
        "reminder_id"
    )

    if reminder_id is None:
        raise AssertionError(
            "reminder_id missing from AIAction output_data."
        )

    reminder = (
        db.query(Reminder)
        .filter(Reminder.id == reminder_id)
        .first()
    )

    if reminder is None:
        raise AssertionError(
            f"Reminder {reminder_id} not found."
        )

    print("\n--- REMINDER ---")
    print("Reminder ID:", reminder.id)
    print("User ID:", reminder.user_id)
    print("Title:", reminder.title)
    print("Remind at:", reminder.remind_at)
    print(
        "Notification channel:",
        reminder.notification_channel,
    )
    print("Status:", reminder.status)

    # Reminder must belong to same user
    assert reminder.user_id == message.user_id

    # Reminder should be pending until notification is sent
    assert reminder.status == "pending"

    # ---------------------------------------------------------
    # 4. Final verification
    # ---------------------------------------------------------
    print("\n===================================")
    print("STEP 24.2 PASSED")
    print("Database relationships verified.")
    print("Message → AIAction → Reminder")
    print("User ownership verified.")
    print("===================================")

finally:
    db.close()