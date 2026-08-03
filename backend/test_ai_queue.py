from app.database.session import SessionLocal
from app.services.ai_message_service import process_pending_ai_messages


db = SessionLocal()

try:
    count = process_pending_ai_messages(
    db=db,
    user_id=1,
    limit=10,
    )

    print(f"Successfully processed: {count}")

finally:
    db.close()