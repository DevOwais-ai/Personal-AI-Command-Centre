from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.contact import (
    ContactCreate,
    ContactResponse,
    ContactUpdate,
)
from app.services.contact_service import (
    create_contact,
    delete_contact,
    get_contact,
    get_contacts,
    update_contact,
)


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)

@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_contact(
        db=db,
        user_id=current_user.id,
        data=data,
    )

@router.get(
    "",
    response_model=list[ContactResponse],
)
def list_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_contacts(
        db=db,
        user_id=current_user.id,
    )

@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
)
def get_single_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = get_contact(
        db=db,
        user_id=current_user.id,
        contact_id=contact_id,
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )

    return contact

@router.patch(
    "/{contact_id}",
    response_model=ContactResponse,
)
def update_existing_contact(
    contact_id: int,
    data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = get_contact(
        db=db,
        user_id=current_user.id,
        contact_id=contact_id,
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )

    return update_contact(
        db=db,
        contact=contact,
        data=data,
    )

@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = get_contact(
        db=db,
        user_id=current_user.id,
        contact_id=contact_id,
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )

    delete_contact(
        db=db,
        contact=contact,
    )

    return None

