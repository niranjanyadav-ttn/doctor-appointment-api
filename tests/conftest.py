"""
Pytest configuration and fixtures for testing.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient
from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.services.auth import AuthService

# Test database URL (use separate test database)
TEST_DATABASE_URL = "mysql+aiomysql://root:rootpassword@localhost:3306/doctor_appointments_test"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test.
    Creates all tables before test and drops them after.
    """
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    # Drop all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create HTTP client for testing API endpoints.
    Overrides the get_db dependency to use test database.
    """
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def doctor_user(db_session: AsyncSession) -> User:
    """Create a test doctor user."""
    hashed_password = AuthService.get_password_hash("doctor123")
    doctor = User(
        email="testdoctor@test.com",
        password_hash=hashed_password,
        name="Dr. Test Doctor",
        role=UserRole.DOCTOR
    )
    db_session.add(doctor)
    await db_session.commit()
    await db_session.refresh(doctor)
    return doctor


@pytest.fixture
async def patient_user(db_session: AsyncSession) -> User:
    """Create a test patient user."""
    hashed_password = AuthService.get_password_hash("patient123")
    patient = User(
        email="testpatient@test.com",
        password_hash=hashed_password,
        name="Test Patient",
        role=UserRole.PATIENT
    )
    db_session.add(patient)
    await db_session.commit()
    await db_session.refresh(patient)
    return patient


@pytest.fixture
async def doctor_token(client: AsyncClient) -> str:
    """Get JWT token for doctor user."""
    # Register doctor
    await client.post(
        "/auth/register",
        json={
            "email": "doctor@test.com",
            "password": "doctor123",
            "name": "Dr. John Smith",
            "role": "Doctor"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "doctor@test.com",
            "password": "doctor123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
async def patient_token(client: AsyncClient) -> str:
    """Get JWT token for patient user."""
    # Register patient
    await client.post(
        "/auth/register",
        json={
            "email": "patient@test.com",
            "password": "patient123",
            "name": "Jane Doe",
            "role": "Patient"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={
            "email": "patient@test.com",
            "password": "patient123"
        }
    )
    return response.json()["access_token"]
