"""
Availability Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime


class AvailabilityBase(BaseModel):
    """Base availability schema."""
    start_time: datetime = Field(..., description="Start time of availability slot")
    end_time: datetime = Field(..., description="End time of availability slot")
    
    @field_validator('end_time')
    @classmethod
    def validate_end_after_start(cls, v: datetime, info) -> datetime:
        """Validate that end_time is after start_time."""
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v
    
    @field_validator('start_time')
    @classmethod
    def validate_start_time_future(cls, v: datetime) -> datetime:
        """Validate that start_time is in the future."""
        if v < datetime.now():
            raise ValueError('start_time must be in the future')
        return v


class AvailabilityCreate(AvailabilityBase):
    """Schema for creating availability."""
    pass


class AvailabilityResponse(AvailabilityBase):
    """Schema for availability response."""
    id: int = Field(..., description="Availability ID")
    doctor_id: int = Field(..., description="Doctor ID")
    
    model_config = ConfigDict(from_attributes=True)
