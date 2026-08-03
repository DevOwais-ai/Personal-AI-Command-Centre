import time

from app.database.session import SessionLocal
from app.services.ai_message_service import (
    process_pending_ai_messages,
    retry_failed_ai_messages,
)


POLL_INTERVAL_SECONDS = 5


def run_ai_worker():
    print("AI worker started.")

    while True:
        db = SessionLocal()

        try:
            # Process pending messages
            processed_count = process_pending_ai_messages(
                db=db,
                user_id=1,
                limit=10,
            )

            if processed_count:
                print(
                    f"Processed {processed_count} message(s)."
                )

            # Retry failed messages
            retry_count = retry_failed_ai_messages(
                db=db,
                limit=10,
            )

            if retry_count:
                print(
                    f"AI worker retried "
                    f"{retry_count} failed message(s)."
                )

        except Exception as exc:
            print(f"AI worker error: {exc}")

        finally:
            db.close()

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_ai_worker()