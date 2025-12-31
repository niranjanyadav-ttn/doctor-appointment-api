"""
Authentication Pydantic schemas.
"""

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Decoded JWT token data."""
    email: str | None = Field(None, description="User email from token")
    role: str | None = Field(None, description="User role from token")


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema."""
    email: EmailStr = Field(..., description="User email for password reset")


class ForgotPasswordResponse(BaseModel):
    """Forgot password response schema."""
    message: str = Field(..., description="Success message")
    reset_token: str = Field(..., description="Password reset token (mock)")
