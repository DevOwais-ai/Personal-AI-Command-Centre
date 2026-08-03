import time

from app.database.session import SessionLocal
from app.services.ai_message_service import (
    process_all_pending_ai_messages,
)


POLL_INTERVAL_SECONDS = 5


def run_ai_worker() -> None:

    print("AI worker started.")

    while True:

        db = SessionLocal()

        try:
            processed_count = process_all_pending_ai_messages(
                db=db,
                limit=10,
            )

            if processed_count:
                print(
                    f"AI worker processed "
                    f"{processed_count} message(s)."
                )

        except Exception as exc:
            print(
                f"AI worker error: {exc}"
            )

        finally:
            db.close()

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_ai_worker()