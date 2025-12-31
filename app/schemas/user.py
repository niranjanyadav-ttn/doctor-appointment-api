"""
User Pydantic schemas for validation and serialization.
"""

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., min_length=2, max_length=255, description="Full name")
    role: UserRole = Field(..., description="User role (Doctor or Patient)")


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100, description="User password")


class UserResponse(UserBase):
    """Schema for user response (excludes password)."""
    id: int = Field(..., description="User ID")
    
    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserBase):
    """Schema for user in database (includes password hash)."""
    id: int
    password_hash: str
    
    model_config = ConfigDict(from_attributes=True)
