from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
)


def create_appointment(
    db: Session,
    user_id: int,
    data: AppointmentCreate,
) -> Appointment:

    appointment = Appointment(
        user_id=user_id,
        title=data.title,
        description=data.description,
        start_at=data.start_at,
        end_at=data.end_at,
        location=data.location,
        contact_id=data.contact_id,
        source="manual",
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


def get_appointments(
    db: Session,
    user_id: int,
) -> list[Appointment]:

    return (
        db.query(Appointment)
        .filter(Appointment.user_id == user_id)
        .order_by(Appointment.start_at.asc())
        .all()
    )


def get_appointment(
    db: Session,
    user_id: int,
    appointment_id: int,
) -> Appointment | None:

    return (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.user_id == user_id,
        )
        .first()
    )


def update_appointment(
    db: Session,
    appointment: Appointment,
    data: AppointmentUpdate,
) -> Appointment:

    updates = data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)

    return appointment


def delete_appointment(
    db: Session,
    appointment: Appointment,
) -> None:

    db.delete(appointment)
    db.commit()