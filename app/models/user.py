"""
User model for authentication and role management.
"""

from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    DOCTOR = "Doctor"
    PATIENT = "Patient"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False)
    
    # Relationships
    availabilities = relationship(
        "Availability",
        back_populates="doctor",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    appointments_as_doctor = relationship(
        "Appointment",
        foreign_keys="[Appointment.doctor_id]",
        back_populates="doctor",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    appointments_as_patient = relationship(
        "Appointment",
        foreign_keys="[Appointment.patient_id]",
        back_populates="patient",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
