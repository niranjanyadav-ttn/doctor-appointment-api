"""
Authentication dependencies for FastAPI.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.models.user import User, UserRole

# HTTP Bearer security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
    
    Returns:
        Current user
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode token
    payload = AuthService.decode_access_token(token)
    email: str = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_doctor(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they are a doctor.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Current user (verified as doctor)
    
    Raises:
        HTTPException: If user is not a doctor
    """
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors can access this endpoint"
        )
    return current_user


async def get_current_patient(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they are a patient.
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Current user (verified as patient)
    
    Raises:
        HTTPException: If user is not a patient
    """
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can access this endpoint"
        )
    return current_user
