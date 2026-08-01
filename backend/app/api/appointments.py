from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)
from app.services.appointment_service import (
    create_appointment,
    delete_appointment,
    get_appointment,
    get_appointments,
    update_appointment,
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
)
from app.services.appointment_service import (
    create_appointment,
    delete_appointment,
    get_appointment,
    get_appointments,
    update_appointment,
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)

@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_appointment(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "",
    response_model=list[AppointmentResponse],
)
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_appointments(
        db=db,
        user_id=current_user.id,
    )

@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_appointment(
        db=db,
        user_id=current_user.id,
        data=data,
    )

@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_appointment(
        db=db,
        user_id=current_user.id,
        data=data,
    )

@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def get_single_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = get_appointment(
        db=db,
        user_id=current_user.id,
        appointment_id=appointment_id,
    )

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    return appointment

@router.patch(
    "/{appointment_id}",
    response_model=AppointmentResponse,
)
def update_existing_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = get_appointment(
        db=db,
        user_id=current_user.id,
        appointment_id=appointment_id,
    )

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    return update_appointment(
        db=db,
        appointment=appointment,
        data=data,
    )

@router.delete(
    "/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = get_appointment(
        db=db,
        user_id=current_user.id,
        appointment_id=appointment_id,
    )

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    delete_appointment(
        db=db,
        appointment=appointment,
    )

    return None

