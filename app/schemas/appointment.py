"""
Appointment Pydantic schemas.
"""

from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from app.models.appointment import AppointmentStatus


class AppointmentBase(BaseModel):
    """Base appointment schema."""
    start_time: datetime = Field(..., description="Appointment start time")
    end_time: datetime = Field(..., description="Appointment end time")
    
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


class AppointmentCreate(AppointmentBase):
    """Schema for creating appointment."""
    doctor_id: int = Field(..., description="Doctor ID to book with")


class AppointmentResponse(AppointmentBase):
    """Schema for appointment response."""
    id: int = Field(..., description="Appointment ID")
    doctor_id: int = Field(..., description="Doctor ID")
    patient_id: int = Field(..., description="Patient ID")
    status: AppointmentStatus = Field(..., description="Appointment status")
    
    model_config = ConfigDict(from_attributes=True)


class AppointmentCancel(BaseModel):
    """Schema for canceling appointment."""
    appointment_id: int = Field(..., description="Appointment ID to cancel")
