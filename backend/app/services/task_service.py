from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    user_id: int,
    data: TaskCreate,
) -> Task:

    task = Task(
        user_id=user_id,
        title=data.title,
        description=data.description,
        priority=data.priority,
        due_at=data.due_at,
        source="manual",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    user_id: int,
) -> list[Task]:

    return (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .all()
    )


def get_task(
    db: Session,
    user_id: int,
    task_id: int,
) -> Task | None:

    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == user_id,
        )
        .first()
    )


def update_task(
    db: Session,
    task: Task,
    data: TaskUpdate,
) -> Task:

    updates = data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(task, field, value)

    if task.status == "completed" and task.completed_at is None:
        task.completed_at = datetime.now(timezone.utc)

    elif task.status != "completed":
        task.completed_at = None

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
) -> None:

    db.delete(task)
    db.commit()