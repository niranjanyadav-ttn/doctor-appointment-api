"""
Tests for database models.
"""

import pytest
from app.models.user import User, UserRole
from app.models.availability import Availability
from app.models.appointment import Appointment, AppointmentStatus
from datetime import datetime, timedelta


class TestUserModel:
    """Test User model."""
    
    @pytest.mark.asyncio
    async def test_create_doctor(self, db_session):
        """Test creating a doctor user."""
        doctor = User(
            email="doctor@test.com",
            password_hash="hashed_password",
            name="Dr. Smith",
            role=UserRole.DOCTOR
        )
        db_session.add(doctor)
        await db_session.commit()
        await db_session.refresh(doctor)
        
        assert doctor.id is not None
        assert doctor.email == "doctor@test.com"
        assert doctor.role == UserRole.DOCTOR
    
    @pytest.mark.asyncio
    async def test_create_patient(self, db_session):
        """Test creating a patient user."""
        patient = User(
            email="patient@test.com",
            password_hash="hashed_password",
            name="John Doe",
            role=UserRole.PATIENT
        )
        db_session.add(patient)
        await db_session.commit()
        await db_session.refresh(patient)
        
        assert patient.id is not None
        assert patient.role == UserRole.PATIENT


class TestAvailabilityModel:
    """Test Availability model."""
    
    @pytest.mark.asyncio
    async def test_create_availability(self, db_session, doctor_user):
        """Test creating availability for doctor."""
        # Use datetime without microseconds to match database precision
        start_time = (datetime.now() + timedelta(days=1)).replace(microsecond=0)
        end_time = (start_time + timedelta(hours=8)).replace(microsecond=0)
        
        availability = Availability(
            doctor_id=doctor_user.id,
            start_time=start_time,
            end_time=end_time
        )
        db_session.add(availability)
        await db_session.commit()
        await db_session.refresh(availability)
        
        assert availability.id is not None
        assert availability.doctor_id == doctor_user.id
        assert availability.start_time == start_time


class TestAppointmentModel:
    """Test Appointment model."""
    
    @pytest.mark.asyncio
    async def test_create_appointment(self, db_session, doctor_user, patient_user):
        """Test creating an appointment."""
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        appointment = Appointment(
            doctor_id=doctor_user.id,
            patient_id=patient_user.id,
            start_time=start_time,
            end_time=end_time,
            status=AppointmentStatus.CONFIRMED
        )
        db_session.add(appointment)
        await db_session.commit()
        await db_session.refresh(appointment)
        
        assert appointment.id is not None
        assert appointment.status == AppointmentStatus.CONFIRMED
