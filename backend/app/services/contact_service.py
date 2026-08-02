from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import (
    ContactCreate,
    ContactUpdate,
)


def create_contact(
    db: Session,
    user_id: int,
    data: ContactCreate,
) -> Contact:

    contact = Contact(
        user_id=user_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        notes=data.notes,
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_contacts(
    db: Session,
    user_id: int,
) -> list[Contact]:

    return (
        db.query(Contact)
        .filter(Contact.user_id == user_id)
        .order_by(Contact.name.asc())
        .all()
    )


def get_contact(
    db: Session,
    user_id: int,
    contact_id: int,
) -> Contact | None:

    return (
        db.query(Contact)
        .filter(
            Contact.id == contact_id,
            Contact.user_id == user_id,
        )
        .first()
    )


def update_contact(
    db: Session,
    contact: Contact,
    data: ContactUpdate,
) -> Contact:

    updates = data.model_dump(
        exclude_unset=True,
    )

    for field, value in updates.items():
        setattr(contact, field, value)

    db.commit()
    db.refresh(contact)

    return contact


def delete_contact(
    db: Session,
    contact: Contact,
) -> None:

    db.delete(contact)
    db.commit()