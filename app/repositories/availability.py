"""
Availability repository for database operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.availability import Availability
from datetime import datetime
from typing import List, Optional


class AvailabilityRepository:
    """Repository for Availability database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_availability(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> Availability:
        """
        Create a new availability slot.
        
        Args:
            doctor_id: Doctor user ID
            start_time: Start time of availability
            end_time: End time of availability
        
        Returns:
            Created Availability object
        """
        availability = Availability(
            doctor_id=doctor_id,
            start_time=start_time,
            end_time=end_time
        )
        self.db.add(availability)
        await self.db.commit()
        await self.db.refresh(availability)
        return availability
    
    async def get_doctor_availabilities(
        self,
        doctor_id: int,
        start_date: Optional[datetime] = None
    ) -> List[Availability]:
        """
        Get all availability slots for a doctor.
        
        Args:
            doctor_id: Doctor user ID
            start_date: Optional filter for availabilities after this date
        
        Returns:
            List of Availability objects
        """
        query = select(Availability).where(Availability.doctor_id == doctor_id)
        
        if start_date:
            query = query.where(Availability.start_time >= start_date)
        
        query = query.order_by(Availability.start_time)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def check_availability_overlap(
        self,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_id: Optional[int] = None
    ) -> bool:
        """
        Check if a time slot overlaps with existing availability.
        
        Args:
            doctor_id: Doctor user ID
            start_time: Start time to check
            end_time: End time to check
            exclude_id: Optional availability ID to exclude from check
        
        Returns:
            True if overlap exists, False otherwise
        """
        query = select(Availability).where(
            and_(
                Availability.doctor_id == doctor_id,
                Availability.start_time < end_time,
                Availability.end_time > start_time
            )
        )
        
        if exclude_id:
            query = query.where(Availability.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
    
    async def get_availability_by_id(self, availability_id: int) -> Optional[Availability]:
        """
        Get availability by ID.
        
        Args:
            availability_id: Availability ID
        
        Returns:
            Availability object or None
        """
        result = await self.db.execute(
            select(Availability).where(Availability.id == availability_id)
        )
        return result.scalar_one_or_none()
