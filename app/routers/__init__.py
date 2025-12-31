"""
Routers package for FastAPI endpoints.
"""

from app.routers import auth, doctors, appointments

__all__ = [
    "auth",
    "doctors",
    "appointments",
]
