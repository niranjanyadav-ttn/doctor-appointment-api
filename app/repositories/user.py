"""
User repository for database operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User, UserRole
from typing import List, Optional


class UserRepository:
    """Repository for User database operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(
        self,
        email: str,
        password_hash: str,
        name: str,
        role: UserRole
    ) -> User:
        """
        Create a new user.
        """
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            role=role
        )
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            await self.db.rollback()
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_doctors(self) -> List[User]:
        """
        Get all users with Doctor role.
        
        Returns:
            List of Doctor users
        """
        result = await self.db.execute(
            select(User).where(User.role == UserRole.DOCTOR)
        )
        return list(result.scalars().all())
