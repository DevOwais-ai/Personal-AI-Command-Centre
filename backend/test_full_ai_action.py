from app.database.session import SessionLocal
from app.models.message import Message
from app.services.ai_message_service import analyze_and_save_message


db = SessionLocal()

try:
    message = Message(
        user_id=1,
        conversation_id=1,
        platform="gmail",
        external_id="step22-integration-test-001",
        direction="incoming",
        sender_name="Test Client",
        sender_identifier="test_client",
        recipient_identifier="owais",
        content="Please remind me tomorrow at 10 AM to send the client proposal.",
        message_type="text",
        is_read=False,
        is_important=False,
        ai_processed=False,
        ai_status="pending",
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    result = analyze_and_save_message(
        db=db,
        message=message,
    )

    print("Message ID:", message.id)
    print("AI status:", message.ai_status)
    print("AI processed:", message.ai_processed)
    print("Intent:", message.ai_intent)
    print("Action required:", message.ai_action_required)

finally:
    db.close()