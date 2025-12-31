"""
Doctor service for doctor-specific operations.
"""

from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from app.repositories.availability import AvailabilityRepository
from app.repositories.appointment import AppointmentRepository
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.schemas.appointment import AppointmentResponse


class DoctorService:
    """Service for doctor operations."""
    
    def __init__(
        self,
        availability_repo: AvailabilityRepository,
        appointment_repo: AppointmentRepository
    ):
        self.availability_repo = availability_repo
        self.appointment_repo = appointment_repo
    
    async def set_availability(
        self,
        doctor_id: int,
        availability_data: AvailabilityCreate
    ) -> AvailabilityResponse:
        """
        Set availability for a doctor.
        
        Args:
            doctor_id: Doctor user ID
            availability_data: Availability data
        
        Returns:
            Created availability
        
        Raises:
            HTTPException: If availability overlaps with existing slots
        """
        # Check for overlap with existing availability
        has_overlap = await self.availability_repo.check_availability_overlap(
            doctor_id=doctor_id,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time
        )
        
        if has_overlap:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Availability slot overlaps with existing availability"
            )
        
        # Create availability
        availability = await self.availability_repo.create_availability(
            doctor_id=doctor_id,
            start_time=availability_data.start_time,
            end_time=availability_data.end_time
        )
        
        return AvailabilityResponse.model_validate(availability)
    
    async def get_my_availabilities(
        self,
        doctor_id: int,
        start_date: datetime | None = None
    ) -> List[AvailabilityResponse]:
        """
        Get doctor's availability slots.
        
        Args:
            doctor_id: Doctor user ID
            start_date: Optional filter for future availabilities
        
        Returns:
            List of availability responses
        """
        availabilities = await self.availability_repo.get_doctor_availabilities(
            doctor_id=doctor_id,
            start_date=start_date
        )
        
        return [AvailabilityResponse.model_validate(a) for a in availabilities]
    
    async def get_my_appointments(
        self,
        doctor_id: int,
        start_date: datetime | None = None
    ) -> List[AppointmentResponse]:
        """
        Get doctor's appointments.
        
        Args:
            doctor_id: Doctor user ID
            start_date: Optional filter for future appointments
        
        Returns:
            List of appointment responses
        """
        appointments = await self.appointment_repo.get_doctor_appointments(
            doctor_id=doctor_id,
            start_date=start_date or datetime.now()
        )
        
        return [AppointmentResponse.model_validate(a) for a in appointments]
