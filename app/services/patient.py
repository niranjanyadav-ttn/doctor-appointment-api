"""
Patient service for patient-specific operations.
"""

from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.repositories.availability import AvailabilityRepository
from app.repositories.appointment import AppointmentRepository
from app.schemas.user import UserResponse
from app.schemas.availability import AvailabilityResponse
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.models.user import UserRole


class PatientService:
    """Service for patient operations."""
    
    def __init__(
        self,
        user_repo: UserRepository,
        availability_repo: AvailabilityRepository,
        appointment_repo: AppointmentRepository
    ):
        self.user_repo = user_repo
        self.availability_repo = availability_repo
        self.appointment_repo = appointment_repo
    
    async def get_all_doctors(self) -> List[UserResponse]:
        """
        Get list of all doctors.
        
        Returns:
            List of doctor user responses
        """
        doctors = await self.user_repo.get_all_doctors()
        return [UserResponse.model_validate(d) for d in doctors]
    
    async def get_doctor_availability(
        self,
        doctor_id: int,
        start_date: datetime | None = None
    ) -> List[AvailabilityResponse]:
        """
        Get availability slots for a specific doctor.
        
        Args:
            doctor_id: Doctor user ID
            start_date: Optional filter for future availabilities
        
        Returns:
            List of availability responses
        
        Raises:
            HTTPException: If doctor not found
        """
        # Verify doctor exists
        doctor = await self.user_repo.get_user_by_id(doctor_id)
        if not doctor or doctor.role != UserRole.DOCTOR:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        availabilities = await self.availability_repo.get_doctor_availabilities(
            doctor_id=doctor_id,
            start_date=start_date or datetime.now()
        )
        
        return [AvailabilityResponse.model_validate(a) for a in availabilities]
    
    async def book_appointment(
        self,
        patient_id: int,
        appointment_data: AppointmentCreate
    ) -> AppointmentResponse:
        """
        Book an appointment with a doctor.
        
        Args:
            patient_id: Patient user ID
            appointment_data: Appointment data
        
        Returns:
            Created appointment
        
        Raises:
            HTTPException: If doctor not found, time slot not available, or booking conflict
        """
        # Verify doctor exists
        doctor = await self.user_repo.get_user_by_id(appointment_data.doctor_id)
        if not doctor or doctor.role != UserRole.DOCTOR:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        # Check if time slot is within doctor's availability
        has_availability = await self._check_time_within_availability(
            doctor_id=appointment_data.doctor_id,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time
        )
        
        if not has_availability:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected time slot is not within doctor's availability"
            )
        
        # Check for booking conflicts (double-booking prevention)
        has_conflict = await self.appointment_repo.check_booking_conflict(
            doctor_id=appointment_data.doctor_id,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time
        )
        
        if has_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This time slot is already booked. Please choose another time."
            )
        
        # Create appointment
        appointment = await self.appointment_repo.create_appointment(
            doctor_id=appointment_data.doctor_id,
            patient_id=patient_id,
            start_time=appointment_data.start_time,
            end_time=appointment_data.end_time
        )
        
        return AppointmentResponse.model_validate(appointment)
    
    async def _check_time_within_availability(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        """
        Check if requested time is within doctor's availability.
        
        Args:
            doctor_id: Doctor user ID
            start_time: Appointment start time
            end_time: Appointment end time
        
        Returns:
            True if time is within availability, False otherwise
        """
        availabilities = await self.availability_repo.get_doctor_availabilities(
            doctor_id=doctor_id
        )
        
        for availability in availabilities:
            if (availability.start_time <= start_time and
                availability.end_time >= end_time):
                return True
        
        return False
    
    async def cancel_appointment(
        self,
        appointment_id: int,
        patient_id: int
    ) -> AppointmentResponse:
        """
        Cancel an appointment.
        
        Args:
            appointment_id: Appointment ID
            patient_id: Patient user ID (for verification)
        
        Returns:
            Cancelled appointment
        
        Raises:
            HTTPException: If appointment not found or patient is not the owner
        """
        # Get appointment
        appointment = await self.appointment_repo.get_appointment_by_id(appointment_id)
        
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )
        
        # Verify patient owns this appointment
        if appointment.patient_id != patient_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own appointments"
            )
        
        # Cancel appointment
        cancelled = await self.appointment_repo.cancel_appointment(appointment_id)
        
        return AppointmentResponse.model_validate(cancelled)
    
    async def get_my_appointments(
        self,
        patient_id: int,
        start_date: datetime | None = None
    ) -> List[AppointmentResponse]:
        """
        Get patient's appointments.
        
        Args:
            patient_id: Patient user ID
            start_date: Optional filter for future appointments
        
        Returns:
            List of appointment responses
        """
        appointments = await self.appointment_repo.get_patient_appointments(
            patient_id=patient_id,
            start_date=start_date or datetime.now()
        )
        
        return [AppointmentResponse.model_validate(a) for a in appointments]
