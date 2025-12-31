"""
Authentication service with JWT and password hashing.
"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token
from app.models.user import User, UserRole
from app.config import settings
from fastapi import HTTPException, status


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against hashed password."""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password using bcrypt."""
        # Truncate to 72 bytes (bcrypt limit)
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        
        Args:
            data: Data to encode in token
            expires_delta: Optional custom expiration time
        
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str) -> dict:
        """
        Decode and verify JWT token.
        
        Args:
            token: JWT token to decode
        
        Returns:
            Decoded token data
        
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
        
        Returns:
            Created user response
        
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = self.get_password_hash(user_data.password)
        
        # Create user
        user = await self.user_repo.create_user(
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name,
            role=user_data.role
        )
        
        return UserResponse.model_validate(user)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
        
        Returns:
            User object if authenticated, None otherwise
        """
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
    
    async def login(self, email: str, password: str) -> Token:
        """
        Login user and return JWT token.
        
        Args:
            email: User email
            password: User password
        
        Returns:
            JWT token
        
        Raises:
            HTTPException: If credentials are invalid
        """
        user = await self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = self.create_access_token(
            data={"sub": user.email, "role": user.role.value}
        )
        
        return Token(access_token=access_token, token_type="bearer")
