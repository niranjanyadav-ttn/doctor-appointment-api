"""
Doctors router for doctor-specific operations.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from app.database import get_db
from app.dependencies.auth import get_current_doctor, get_current_user
from app.repositories.user import UserRepository
from app.repositories.availability import AvailabilityRepository
from app.repositories.appointment import AppointmentRepository
from app.services.doctor import DoctorService
from app.services.patient import PatientService
from app.schemas.user import UserResponse
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.schemas.appointment import AppointmentResponse
from app.models.user import User

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get(
    "",
    response_model=List[UserResponse],
    summary="Get all doctors",
    description="Get list of all registered doctors (accessible by anyone)"
)
async def get_all_doctors(
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all doctors.
    
    Returns list of all users with Doctor role.
    No authentication required.
    """
    user_repo = UserRepository(db)
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    patient_service = PatientService(user_repo, availability_repo, appointment_repo)
    
    return await patient_service.get_all_doctors()


@router.get(
    "/{doctor_id}/availability",
    response_model=List[AvailabilityResponse],
    summary="Get doctor's availability",
    description="Get availability slots for a specific doctor"
)
async def get_doctor_availability(
    doctor_id: int,
    start_date: datetime | None = Query(None, description="Filter availabilities from this date"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get availability slots for a specific doctor.
    
    - **doctor_id**: Doctor's user ID
    - **start_date**: Optional filter for future availabilities
    
    No authentication required.
    """
    user_repo = UserRepository(db)
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    patient_service = PatientService(user_repo, availability_repo, appointment_repo)
    
    return await patient_service.get_doctor_availability(doctor_id, start_date)


@router.post(
    "/availability",
    response_model=AvailabilityResponse,
    status_code=201,
    summary="Set availability (Doctor only)",
    description="Set availability slot - only accessible by doctors"
)
async def set_availability(
    availability_data: AvailabilityCreate,
    current_user: User = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    """
    Set availability slot for logged-in doctor.
    
    **Requires:** Doctor role
    
    - **start_time**: Start of availability slot (must be in future)
    - **end_time**: End of availability slot (must be after start_time)
    
    Returns created availability slot.
    """
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    doctor_service = DoctorService(availability_repo, appointment_repo)
    
    return await doctor_service.set_availability(current_user.id, availability_data)


@router.get(
    "/my-appointments",
    response_model=List[AppointmentResponse],
    summary="Get my appointments (Doctor only)",
    description="Get all appointments for logged-in doctor"
)
async def get_my_appointments(
    start_date: datetime | None = Query(None, description="Filter appointments from this date"),
    current_user: User = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all appointments for logged-in doctor.
    
    **Requires:** Doctor role
    
    - **start_date**: Optional filter for future appointments
    
    Returns list of confirmed appointments.
    """
    availability_repo = AvailabilityRepository(db)
    appointment_repo = AppointmentRepository(db)
    doctor_service = DoctorService(availability_repo, appointment_repo)
    
    return await doctor_service.get_my_appointments(current_user.id, start_date)
