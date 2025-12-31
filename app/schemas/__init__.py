"""
Pydantic schemas package for request/response validation.
"""

from app.schemas.user import UserBase, UserCreate, UserResponse, UserInDB
from app.schemas.auth import (
    Token,
    TokenData,
    LoginRequest,
    ForgotPasswordRequest,
    ForgotPasswordResponse
)
from app.schemas.availability import (
    AvailabilityBase,
    AvailabilityCreate,
    AvailabilityResponse
)
from app.schemas.appointment import (
    AppointmentBase,
    AppointmentCreate,
    AppointmentResponse,
    AppointmentCancel
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserInDB",
    "Token",
    "TokenData",
    "LoginRequest",
    "ForgotPasswordRequest",
    "ForgotPasswordResponse",
    "AvailabilityBase",
    "AvailabilityCreate",
    "AvailabilityResponse",
    "AppointmentBase",
    "AppointmentCreate",
    "AppointmentResponse",
    "AppointmentCancel",
]
