"""
Tests for service layer business logic.
"""

import pytest
from app.services.auth import AuthService
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.models.user import UserRole


class TestAuthService:
    """Test AuthService."""
    
    @pytest.mark.asyncio
    async def test_password_hashing(self):
        """Test password is properly hashed."""
        password = "testpassword123"
        hashed = AuthService.get_password_hash(password)
        
        assert hashed != password
        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrongpass", hashed) is False
    
    @pytest.mark.asyncio
    async def test_register_user(self, db_session):
        """Test user registration service."""
        user_repo = UserRepository(db_session)
        auth_service = AuthService(user_repo)
        
        user_data = UserCreate(
            email="newuser@test.com",
            password="password123",
            name="New User",
            role=UserRole.PATIENT
        )
        
        user = await auth_service.register_user(user_data)
        
        assert user.email == "newuser@test.com"
        assert user.id is not None
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email_fails(self, db_session):
        """Test registering duplicate email fails."""
        user_repo = UserRepository(db_session)
        auth_service = AuthService(user_repo)
        
        user_data = UserCreate(
            email="duplicate@test.com",
            password="password123",  # Fixed: 8+ characters
            name="Test",
            role=UserRole.PATIENT
        )
        
        await auth_service.register_user(user_data)
        
        with pytest.raises(Exception):
            await auth_service.register_user(user_data)
    
    @pytest.mark.asyncio
    async def test_authenticate_user(self, db_session, patient_user):
        """Test user authentication."""
        user_repo = UserRepository(db_session)
        auth_service = AuthService(user_repo)
        
        user = await auth_service.authenticate_user(
            "testpatient@test.com",
            "patient123"
        )
        
        assert user is not None
        assert user.email == "testpatient@test.com"
    
    @pytest.mark.asyncio
    async def test_authenticate_wrong_password(self, db_session, patient_user):
        """Test authentication with wrong password fails."""
        user_repo = UserRepository(db_session)
        auth_service = AuthService(user_repo)
        
        user = await auth_service.authenticate_user(
            "testpatient@test.com",
            "wrongpassword"
        )
        
        assert user is None
    
    @pytest.mark.asyncio
    async def test_create_access_token(self):
        """Test JWT token creation."""
        token = AuthService.create_access_token(
            data={"sub": "test@test.com", "role": "Patient"}
        )
        
        assert token is not None
        assert len(token) > 0
    
    @pytest.mark.asyncio
    async def test_decode_access_token(self):
        """Test JWT token decoding."""
        token = AuthService.create_access_token(
            data={"sub": "test@test.com", "role": "Doctor"}
        )
        
        payload = AuthService.decode_access_token(token)
        
        assert payload["sub"] == "test@test.com"
        assert payload["role"] == "Doctor"
