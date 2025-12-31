"""
Appointment repository for database operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.models.appointment import Appointment, AppointmentStatus
from datetime import datetime
from typing import List, Optional


class AppointmentRepository:
    """Repository for Appointment database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_appointment(
        self,
        doctor_id: int,
        patient_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> Appointment:

        appointment = Appointment(
            doctor_id=doctor_id,
            patient_id=patient_id,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.CONFIRMED
        )
        self.db.add(appointment)
        await self.db.commit()
        await self.db.refresh(appointment)
        return appointment
    
    async def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        
        result = await self.db.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()
    
    async def get_doctor_appointments(
        self,
        doctor_id: int,
        start_date: Optional[datetime] = None
    ) -> List[Appointment]:
        """
        Get all appointments for a doctor.
        
        Args:
            doctor_id: Doctor user ID
            start_date: Optional filter for appointments after this date
        
        Returns:
            List of Appointment objects
        """
        query = select(Appointment).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.status == AppointmentStatus.CONFIRMED
            )
        )
        
        if start_date:
            query = query.where(Appointment.start_time >= start_date)
        
        query = query.order_by(Appointment.start_time)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_patient_appointments(
        self,
        patient_id: int,
        start_date: Optional[datetime] = None
    ) -> List[Appointment]:
        """
        Get all appointments for a patient.
        
        Args:
            patient_id: Patient user ID
            start_date: Optional filter for appointments after this date
        
        Returns:
            List of Appointment objects
        """
        query = select(Appointment).where(
            and_(
                Appointment.patient_id == patient_id,
                Appointment.status == AppointmentStatus.CONFIRMED
            )
        )
        
        if start_date:
            query = query.where(Appointment.start_time >= start_date)
        
        query = query.order_by(Appointment.start_time)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def check_booking_conflict(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Check if booking time conflicts with existing confirmed appointments.
        
        Args:
            doctor_id: Doctor user ID
            start_time: Proposed start time
            end_time: Proposed end time
            exclude_id: Optional appointment ID to exclude from check
        
        Returns:
            True if conflict exists, False otherwise
        """
        query = select(Appointment).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.status == AppointmentStatus.CONFIRMED,
                Appointment.start_time < end_time,
                Appointment.end_time > start_time
            )
        )
        
        if exclude_id:
            query = query.where(Appointment.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def cancel_appointment(self, appointment_id: int) -> Optional[Appointment]:
        """
        Cancel an appointment by setting status to CANCELLED.
        
        Args:
            appointment_id: Appointment ID
        
        Returns:
            Updated Appointment object or None
        """
        appointment = await self.get_appointment_by_id(appointment_id)
        if appointment:
            appointment.status = AppointmentStatus.CANCELLED
            await self.db.commit()
            await self.db.refresh(appointment)
        return appointment
