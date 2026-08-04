from app.database.session import SessionLocal
from app.models.message import Message
from app.services.ai_message_service import (
    analyze_and_save_message,
    retry_ai_analysis,
)


db = SessionLocal()

try:
    # ---------------------------------------------------------
    # 1. Create a message that will intentionally fail
    # ---------------------------------------------------------
    message = Message(
        user_id=1,
        conversation_id=1,
        platform="test",
        direction="incoming",
        sender_name="Phase 2 Test",
        content="",
        message_type="text",
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    print("Created failure-test message:", message.id)

    # ---------------------------------------------------------
    # 2. Process the invalid message
    # ---------------------------------------------------------
    try:
        analyze_and_save_message(
            db=db,
            message=message,
        )
    except ValueError as exc:
        print("Expected failure:", exc)

    db.refresh(message)

    print("\n--- FAILURE RESULT ---")
    print("Message ID:", message.id)
    print("AI status:", message.ai_status)
    print("AI processed:", message.ai_processed)

    # Failure must be recorded
    assert message.ai_status == "failed"
    assert message.ai_processed is False

    # ---------------------------------------------------------
    # 3. Verify retry is allowed
    # ---------------------------------------------------------
    print("\n--- RETRY TEST ---")

    try:
        retry_ai_analysis(
            db=db,
            message=message,
        )
    except Exception as exc:
        print("Retry result:", exc)

    db.refresh(message)

    print("AI status after retry:", message.ai_status)
    print("AI processed after retry:", message.ai_processed)

    # The empty message will fail again.
    # This is intentional: we are testing retry handling.
    assert message.ai_status == "failed"
    assert message.ai_processed is False

    print("\n===================================")
    print("STEP 24.3 PASSED")
    print("Failure and retry handling verified.")
    print("===================================")

finally:
    db.close()