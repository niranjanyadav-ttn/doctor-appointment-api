"""
Dependencies package for FastAPI dependency injection.
"""

from app.dependencies.auth import (
    get_current_user,
    get_current_doctor,
    get_current_patient
)

__all__ = [
    "get_current_user",
    "get_current_doctor",
    "get_current_patient",
]
