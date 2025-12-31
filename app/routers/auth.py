"""
Authentication router for user registration and login.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import (
    LoginRequest,
    Token,
    ForgotPasswordRequest,
    ForgotPasswordResponse
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user (Doctor or Patient) with email and password"
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 8 characters)
    - **name**: Full name
    - **role**: User role (Doctor or Patient)
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return await auth_service.register_user(user_data)


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    description="Login with email and password to receive JWT token"
)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login user and receive JWT token.
    
    - **email**: User email
    - **password**: User password
    
    Returns JWT access token for authentication.
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return await auth_service.login(login_data.email, login_data.password)


@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse,
    summary="Request password reset",
    description="Request password reset token (mock implementation)"
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset (mock implementation).
    
    In a real application, this would:
    1. Verify email exists
    2. Generate reset token
    3. Send email with reset link
    
    For this demo, it returns a mock reset token.
    """
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(request.email)
    
    if not user:
        # For security, don't reveal if email exists
        return ForgotPasswordResponse(
            message="If the email exists, a reset link has been sent",
            reset_token="mock_reset_token_123456"
        )
    
    # In production: generate real token and send email
    return ForgotPasswordResponse(
        message="Password reset link sent to your email",
        reset_token="mock_reset_token_123456"
    )
