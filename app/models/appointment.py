"""
Appointment model for booking management.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class AppointmentStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doctor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    patient_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    status = Column(
        SQLEnum(AppointmentStatus),
        default=AppointmentStatus.CONFIRMED,
        nullable=False,
        index=True
    )
    
    # Relationships
    doctor = relationship(
        "User",
        foreign_keys=[doctor_id],
        back_populates="appointments_as_doctor"
    )
    patient = relationship(
        "User",
        foreign_keys=[patient_id],
        back_populates="appointments_as_patient"
    )
    
    def __repr__(self) -> str:
        return f"<Appointment(id={self.id}, doctor_id={self.doctor_id}, patient_id={self.patient_id}, status='{self.status}')>"
