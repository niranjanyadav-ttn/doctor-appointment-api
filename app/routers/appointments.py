"""
Appointments router for booking and managing appointments.
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from app.database import get_db
from app.dependencies.auth import get_current_patient, get_current_user
from app.repositories.user import UserRepository
from app.repositories.availability import AvailabilityRepository
from app.repositories.appointment import AppointmentRepository
from app.services.patient import PatientService
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.models.user import User

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=201,
    summary="Book appointment (Patient only)",
    description="Book an appointment with a doctor - only accessible by patients"
)
async def book_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_patient),
    db: AsyncSession = Depends(get_db)
):
    """
    Book an appointment with a doctor.
    
    **Requires:** Patient role
    
    - **doctor_id**: Doctor's user ID
    - **start_time**: Appointment start time (must be in future)
    - **end_time**: Appointment end time (must be after start_time)
    
    **Validations:**
    - Time slot must be within doctor's availability
    - Time slot must not conflict with existing appointments (double-booking prevention)
    
    Returns created appointment.
    """
    user_repo = UserRepository(db)
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    patient_service = PatientService(user_repo, availability_repo, appointment_repo)
    
    return await patient_service.book_appointment(current_user.id, appointment_data)


@router.delete(
    "/{appointment_id}",
    response_model=AppointmentResponse,
    summary="Cancel appointment (Patient only)",
    description="Cancel an appointment - only accessible by the patient who booked it"
)
async def cancel_appointment(
    appointment_id: int = Path(..., description="Appointment ID to cancel"),
    current_user: User = Depends(get_current_patient),
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel an appointment.
    
    **Requires:** Patient role
    
    - **appointment_id**: ID of appointment to cancel
    
    **Validations:**
    - Appointment must exist
    - Patient must be the owner of the appointment
    
    Returns cancelled appointment with status updated to 'cancelled'.
    """
    user_repo = UserRepository(db)
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    patient_service = PatientService(user_repo, availability_repo, appointment_repo)
    
    return await patient_service.cancel_appointment(appointment_id, current_user.id)


@router.get(
    "/my-appointments",
    response_model=List[AppointmentResponse],
    summary="Get my appointments",
    description="Get all appointments for logged-in user (Doctor or Patient)"
)
async def get_my_appointments(
    start_date: datetime | None = Query(None, description="Filter appointments from this date"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all appointments for logged-in user.
    
    **Requires:** Authentication (Doctor or Patient)
    
    - **start_date**: Optional filter for future appointments
    
    Returns list of appointments based on user role:
    - **Doctor**: Returns appointments where user is the doctor
    - **Patient**: Returns appointments where user is the patient
    """
    user_repo = UserRepository(db)
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    patient_service = PatientService(user_repo, availability_repo, appointment_repo)
    
    return await patient_service.get_my_appointments(current_user.id, start_date)
